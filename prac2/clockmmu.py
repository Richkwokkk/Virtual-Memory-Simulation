from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False

        # Dictionary to store the pages currently in memory
        self.memory_map = {}
        # Pointer for the clock hand in the algorithm
        self.clock_pointer = 0
        # Dictionary to keep track of reference bits
        self.ref_bits = {}
        # Dictionary to keep track of dirty bits (whether pages are modified)
        self.dirty_bits = {}
        # List to track the order of pages in memory
        self.page_list = []
        self.debug = False

    def enable_debug(self):
        self.debug_mode = True

    def disable_debug(self):
        self.debug_mode = False

    def read_memory(self, page_id):
        if page_id in self.memory_map:
            # Page is present in memory
            self.ref_bits[page_id] = 1
            if self.debug_mode:
                print(f"Page {page_id} accessed in memory.")
        else:
            # Page fault occurs
            self.page_faults += 1
            if len(self.memory_map) < self.num_frames:
                # Space available in memory
                self.memory_map[page_id] = len(self.memory_map)
                self.page_list.append(page_id)
                if self.debug_mode:
                    print(f"Page {page_id} loaded into memory.")
            else:
                # Memory is full, replace a page
                self.resolve_page_fault(page_id)
            self.disk_reads += 1
            self.ref_bits[page_id] = 1
            self.dirty_bits[page_id] = 0

    def write_memory(self, page_id):
        if page_id in self.memory_map:
            # Page is already in memory
            self.ref_bits[page_id] = 1
            self.dirty_bits[page_id] = 1
            if self.debug_mode:
                print(f"Page {page_id} written to memory.")
        else:
            # Page fault occurs
            self.page_faults += 1
            if len(self.memory_map) < self.num_frames:
                # Space available in memory
                self.memory_map[page_id] = len(self.memory_map)
                self.page_list.append(page_id)
                if self.debug_mode:
                    print(f"Page {page_id} loaded into memory.")
            else:
                # Memory is full, replace a page
                self.resolve_page_fault(page_id)
            self.disk_reads += 1
            self.ref_bits[page_id] = 1
            self.dirty_bits[page_id] = 1

    def resolve_page_fault(self, new_page):
        while True:
            # Select the page to be replaced based on the clock hand
            candidate_page = self.page_list[self.clock_pointer]
            if self.ref_bits[candidate_page] == 0:
                # The page is not recently used
                if self.dirty_bits[candidate_page] == 1:
                    # Increment disk writes if the page was modified
                    self.disk_writes += 1
                if self.debug_mode:
                    print(f"Replacing page {candidate_page} with new page {new_page}.")
                # Replace the candidate page with the new page
                del self.memory_map[candidate_page]
                self.memory_map[new_page] = self.clock_pointer
                self.page_list[self.clock_pointer] = new_page
                self.ref_bits[new_page] = 1
                self.dirty_bits[new_page] = 0
                self.clock_pointer = (self.clock_pointer + 1) % self.num_frames
                break
            else:
                # Provide a second chance to the page
                self.ref_bits[candidate_page] = 0
                self.clock_pointer = (self.clock_pointer + 1) % self.num_frames

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
