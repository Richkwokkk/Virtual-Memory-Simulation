from mmu import MMU

class ClockMMU(MMU):
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

        # Clock hand pointer to track the next page to be replaced
        self.clock_hand = 0

        # Use bits to track the second chance status of pages
        self.use_bits = []

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        # Check if the page is already in memory
        if page_number in self.page_table:
            # Find the index of the page in memory and set its use bit to 1 (mark it as recently used)
            frame_index = self.memory.index(page_number)
            self.use_bits[frame_index] = 1
            
            if self.debug_mode:
                print(f"Page {page_number} has been read from memory.")
        
        # If the page is not in memory, it's a page fault
        else:
            self.page_faults += 1
            self.handle_page_fault(page_number, mode='R')
            if self.debug_mode:
                print(f"Fail to read page {page_number} from memory.")

    def write_memory(self, page_number):
        # Check if the page is already in memory
        if page_number in self.page_table:
            # Find the index of the page in memory and set its use bit to 1 (mark it as recently used)
            frame_index = self.memory.index(page_number)
            self.use_bits[frame_index] = 1
            
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
        # If memory is full, use the clock algorithm to replace a page
        if len(self.memory) == self.frames:
            while True:
                # Check if the current page pointed to by the clock hand has a use bit of 0
                if self.use_bits[self.clock_hand] == 0:
                    # If the use bit is 0, replace this page
                    page_to_evict = self.memory[self.clock_hand]

                    # If the evicted page was written to, increment disk writes
                    if self.page_table[page_to_evict] == 'W':
                        self.disk_writes += 1
                    
                    # Replace the evicted page with the new page
                    self.memory[self.clock_hand] = page_number
                    self.page_table[page_number] = mode
                    del self.page_table[page_to_evict]
                    self.use_bits[self.clock_hand] = 1

                    if self.debug_mode:
                        print(f"Page fault: page {page_number} has been loaded into frame {self.clock_hand}, replacing page {page_to_evict}.")
                    
                    # Exit the loop after handling the page fault
                    break
                
                else:
                    # If the use bit is 1, set it to 0 (give the page a second chance)
                    self.use_bits[self.clock_hand] = 0

                    # Move the clock hand to the next frame (circular movement)
                    self.clock_hand = (self.clock_hand + 1) % self.frames
        
        else:
            # If there is still space in memory, simply add the page
            self.memory.append(page_number)
            self.use_bits.append(1)
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
