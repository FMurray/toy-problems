#[derive(Debug)]
pub struct Stack<T> {
    items: Vec<T>
}

pub impl<T> Stack {
    fn new(&self) -> Self {
        self.items = Vec::new()
    }

    fn push(&mut self, item: T) {
        self.items
    }
}