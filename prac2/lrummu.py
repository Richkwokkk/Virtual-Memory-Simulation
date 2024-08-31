from mmu import MMU
from collections import OrderedDict

class LruMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False

        # Memory to store pages (initially empty)
        self.memory = []

        # Page table as an ordered dictionary to keep track of the order of pages (LRU)
        self.page_table = OrderedDict()

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        # Check if the page is already in memory
        if page_number in self.page_table:

            # Move the page to the end of the ordered dictionary to mark it as recently used
            self.page_table.move_to_end(page_number)
            
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
            self.page_table.move_to_end(page_number)
            
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
        # If memory is full, replace the least recently used page
        if len(self.memory) == self.frames:

            # Remove the least recently used page (in FIFO order if last is false)
            page_to_evict, page_to_evict_mode = self.page_table.popitem(last=False)
            self.memory.remove(page_to_evict)

            # If the evicted page was written to, increment disk writes
            if page_to_evict_mode == 'W':
                self.disk_writes += 1
            
            # Add the new page to memory and update the page table
            self.memory.append(page_number)
            self.page_table[page_number] = mode
            
            if self.debug_mode:
                print(f"Page fault: page {page_number} has been loaded into memory, replacing LRU page {page_to_evict}.")
        
        # If there is still space in memory, simply add the page
        else:
            self.memory.append(page_number)
            self.page_table[page_number] = mode
            
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
