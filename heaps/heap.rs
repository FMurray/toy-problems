use core::mem::{self, swap, ManuallyDrop};

pub struct Heap<T> {
    data: Vec<T>,
}

impl<T: Ord> Heap<T> {
    pub fn new() -> Heap<T> {
        Heap { data: vec![] }
    }

    pub fn push(&mut self, item: T) {
        let old_len = self.len();
        self.data.push(item);

        unsafe { self.sift_up(0, old_len) };
    }

    unsafe fn sift_up(&mut self, start: usize, pos: usize) -> usize {
        let mut hole = unsafe { Hole::new(&mut self.data, pos) };

        while hole.pos() > start {
            let parent = (hole.pos() - 1) / 2;

            if hole.element() <= unsafe { hole.get(parent) } {
                break;
            }

            unsafe { hole.move_to(parent) }
        }

        hole.pos()
    }
}

struct Hole<'a, T: 'a> {
    data: &'a mut [T],
    elt: ManuallyDrop<T>,
    pos: usize,
}

impl<'a, T> Hole<'a, T> {
    unsafe fn new(data: &'a mut [T], pos: usize) -> Self {
        debug_assert!(pos < data.len());

        let elt = unsafe { ptr::read(data.get_unchecked(pos)) };
        Hole {
            data,
            elt: ManuallyDrop::new(elt),
            pos,
        }
    }

    fn pos(&self) -> usize {
        self.pos
    }

    fn element(&self) -> &T {
        &self.elt
    }

    unsafe fn get(&self, index: usize) -> &T {
        debug_assert!(index != self.pos);
        debug_assert!(index < self.data.len());
        unsafe { self.data.get_unchecked(index) }
    }

    unsafe fn move_to(&mut self, index: usize) {
        debug_assert!(index != self.pos);
        debug_assert!(index < self.data.len());

        unsafe {
            let ptr = self.data.as_mut_ptr();
            let index_ptr: *const _ = ptr.add(index);
            let hole_ptr = ptr.add(self.pos);
            ptr::copy_nonoverlapping(index_ptr, hole_ptr, 1);
        }
        self.pos = index;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1() {
        let mut h = Heap::new();
        h.push(1)
    }
}
