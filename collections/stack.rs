#[derive(Debug)]
pub struct Stack<T> {
    items: Vec<T>
}

impl<T> Stack <T> {
    fn new() -> Self {
        Stack {
            items: Vec::new()
        }
    }

    fn push(&mut self, item: T) {
        self.items.push(item);
    }
}

fn main() {
    let s: Stack<usize> = Stack::new();
    println!("Made a stack!!")
}