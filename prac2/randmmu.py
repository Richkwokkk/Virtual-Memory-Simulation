from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False

        # Memory to store pages (initially empty)
        self.memory = []

        # Page table to track pages in memory and their states (read/write)
        self.page_table = {}

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        # Check if the page is already in memory
        if page_number in self.page_table:
            if self.debug_mode:
                print(f"Page {page_number} has been read from memory.")
        
        # If the page is not in memory, it's a page fault
        else:
            if self.debug_mode:
                print(f"Fail to read page {page_number} from memory.")
            
            self.page_faults += 1
            self.handle_page_fault(page_number, mode='R')

    def write_memory(self, page_number):
        # Check if the page is already in memory
        if page_number in self.page_table:
            if self.debug_mode:
                print(f"Page {page_number} has been written to memory.")
            
            # Mark the page as 'W' (written)
            self.page_table[page_number] = 'W'
        
        # If the page is not in memory, it's a page fault
        else:
            if self.debug_mode:
                print(f"Fail to write page {page_number} to memory.") 
            
            self.page_faults += 1
            self.handle_page_fault(page_number, mode='W')

    def handle_page_fault(self, page_number, mode):
        # If memory is full, replace a random page
        if len(self.memory) == self.frames:
            replaced_index = random.randint(0, self.frames-1)
            page_to_evict = self.memory[replaced_index]

            # If the evicted page was written to, increment disk writes
            if self.page_table[page_to_evict] == 'W':
                self.disk_writes += 1
            
            # Replace the evicted page with the new page
            self.memory[replaced_index] = page_number
            del self.page_table[page_to_evict]

            # Add the new page to the page table with the appropriate mode (read/write)
            self.page_table[page_number] = mode
            if self.debug_mode:
                print(f"Page fault: page {page_number} has been loaded into frame {replaced_index}.")
        
        # If there is still space in memory, simply add the page
        else:
            self.memory.append(page_number)
            self.page_table[page_number] = mode
            replaced_index = len(self.memory) - 1
            
            if self.debug_mode:
                print(f"Page fault: page {page_number} has been loaded into memory.")

        # Increment disk reads when a new page is loaded into memory
        self.disk_reads += 1

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
