import pyshark
import socket
import psutil
import struct
import os
import keyboard
from datetime import datetime
import csv
import traceback
import MarketPlace_pb2 as MarketPlace_pb2
from macros import *
import scheme
import image

class MarketCapture:
    MARKET_PROTO = 3512
    RANDOM_PADDING = 256

    def __init__(self, interface='Ethernet', port_range=(20200, 20300)):
        self.running = True
        self.capture_image = True
        self.data_dir = os.path.join("data")
        self.image_dir = os.path.join(self.data_dir, "images")
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.data_file_name = os.path.join(self.data_dir, f"{self.current_date}.csv")
        self.image_text_file = os.path.join(self.data_dir, f"{self.current_date}.txt")
        self.base_image_path = os.path.join(self.image_dir, "base_image_1920x1080.png")
        self.count = 0
        self.errors = 0
        self.interface = interface
        self.port_range = port_range
        self.last_refresh = datetime.now()
        self.seconds_before_force_refresh = 10
        keyboard.add_hotkey('f7', self.stop_running)
    
    def capture(self):
        local_ip = self.get_local_ip()
        if not local_ip:
            print(f"Could not find IP address for interface {self.interface}")
            return

        capture = pyshark.LiveCapture(
            interface=self.interface,
            display_filter=f'ip.dst == {local_ip} and tcp.srcport >= {self.port_range[0]} and tcp.srcport <= {self.port_range[1]}'
        )


        try:
            self.process_packets(capture)
        except KeyboardInterrupt:
            print("\nCapture stopped by user.")
            self.errors += 1
        except EOFError:
            print("Stream closed unexpectedly.")
            self.errors += 1
        except Exception as e:
            print(f"An unexpected error occurred while capturing: {e}")
            self.errors += 1

    def process_packets(self, capture):
        packet_data = b""
        
        for packet in capture.sniff_continuously():
            if not self.running:
                return
            
            current_time = datetime.now()
            if (current_time - self.last_refresh).seconds > self.seconds_before_force_refresh:
                self.refresh_hook()

            if 'TCP' in packet and hasattr(packet.tcp, 'payload'):
                payload = packet.tcp.payload.binary_value
                if len(payload) <= 8:
                    continue
                
                packet_data += payload

                try:
                    packet_length, proto_type, random_padding = struct.unpack('<IHH', packet_data[:8]) # Packet header
                except struct.error:
                    print("HEADER UNPACK ERROR")
                    packet_data = b""
                    self.errors += 1
                    self.refresh_hook()
                    continue

                if proto_type == self.MARKET_PROTO and random_padding == self.RANDOM_PADDING:
                    if len(packet_data) == packet_length:
                        self.parse_market(packet_data[8:])
                        packet_data = b""
                    elif len(packet_data) > packet_length:
                        print(f"PACKET LENGTH ERROR: len({len(packet_data)}) > {packet_length}")
                        self.errors += 1
                        packet_data = b""
                        self.refresh_hook()
                else:
                    packet_data = b""

    def parse_market(self, data):
        try:
            info = MarketPlace_pb2.SS2C_MARKETPLACE_ITEM_LIST_RES() # Protobuf
            info.ParseFromString(data)
        except Exception as e:
            print(f"An unexpected error occurred while parsing: {e}")
            self.errors += 1
        
        self.save(info)

        self.refresh_hook()
    
    def save(self, info):
        for index, item_info in enumerate(info.itemInfos):
            parts = item_info.item.itemId.split("_")
            name = parts[-2]
            # TODO
            # An unexpected error occurred while capturing: list index out of range
            # An unexpected error occurred while capturing: dict contains fields not in fieldnames: 's_PhysicalDamageRedunData'
            # An unexpected error occurred while capturing: dict contains fields not in fieldnames: ''

            pp = [(p.propertyTypeId, p.propertyValue) for p in item_info.item.primaryPropertyArray]
            sp = [(p.propertyTypeId, p.propertyValue) for p in item_info.item.secondaryPropertyArray]

            if name == "Item": # We want gear not items
                continue

            if not (parts[-1] and parts[-1][0].isdigit()): # Items with no rarity
                continue

            if not pp or not sp: # Items with no propertys
                continue


            rarity_id = int(parts[-1][0]) - 1
            rarity = scheme.property_count_to_rarity[rarity_id]

            item = {
                "name": name,
                "rarity": rarity,
                "price": item_info.price
            }

            if self.capture_image:
                move_to_index(index)
                screenshot = screenshot_section()
                result = image.remove_identical_parts(self.base_image_path, screenshot)
                text = image.image_to_text(result)
                while "\n" in text:
                    text = text.replace("\n", " ")
                text = text.replace('"', " ")
                item["text"] = text

            design_str = "DesignDataItemPropertyType:Id_ItemPropertyType_Effect"

            for property_type in scheme.property_types:
                item[property_type] = 0
            
            for property in pp:
                property_type = property[0].replace(design_str, "p")
                item[property_type] = property[1]

            for property in sp:
                property_type = property[0].replace(design_str, "s")
                item[property_type] = property[1]
            
            self.insert_item(item)

    def insert_item(self, item):
        self.count += 1
        file_exists = os.path.isfile(self.data_file_name)
        with open(self.data_file_name, mode="a", newline="") as file:
            if self.capture_image:
                fieldnames = ["name", "rarity", "price"] + scheme.property_types  + ["text"]
            else:
                fieldnames = ["name", "rarity", "price"] + scheme.property_types
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow(item)
    
    def screenshot_save(self):
        file_exists = os.path.isfile(self.image_text_file)
        screenshot = screenshot_section()
        result = image.remove_identical_parts(self.base_image_path, screenshot)
        text = image.image_to_text(result)
        text = text.replace("\n", " ")
        with open(self.image_text_file, "a") as file:
            if not file_exists:
                file.write("id,text\n")
            file.write(f"{str(self.count)}.{text}\n")

    def refresh_hook(self):
        refresh()
        self.last_refresh = datetime.now()
    
    def stop_running(self):
        print("F7 was pressed! Shutting down!")
        self.running = False
    
    def get_local_ip(self):
        for interface, addrs in psutil.net_if_addrs().items():
            if interface == self.interface:
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        return addr.address
        return None

    def save_image(self, image):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        data_file_name = f"{timestamp}.png"
        file_path = os.path.join(self.image_dir, data_file_name)
        image.save(file_path)
        return file_path

    def run(self):
        start_time = datetime.now().strftime("%H:%M:%S")
        try:
            print("Capturing...")
            while 1: # TODO
                self.capture()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()

        current_time = datetime.now().strftime("%H:%M:%S")
        print("Start Time:", start_time)
        print("Current Time:", current_time)
        print("Errors:", self.errors)
        print("Count:", self.count)

if __name__ == "__main__":
    market_capture = MarketCapture()
    market_capture.run()

