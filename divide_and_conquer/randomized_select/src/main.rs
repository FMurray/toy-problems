fn main() {
}

// fn partition<T: Ord>(x: &mut [T]) -> usize {
//     let l = x.len();
//     let mut store = 0;
//     {
//         let (y, elem) = x.split_at_mut(l - 1);
//         let elem = &mut elem[0];

//         for load in 0..l - 1 {
//             if y[load] < *elem {
//                 y.swap(load, store);
//                 store += 1
//             }
//         }
//     }
//     x.swap(store, l - 1);
//     store
// }

fn median_of_three(list: &Vec<impl PartialOrd>, left: usize, right: usize) -> usize {
    let half_index = right / 2;

    let beginning = &list[left];
    let middle = &list[half_index];
    let end = &list[right];

    let comparison = |median, other_one, other_two| {
        median > other_one && median < other_two || median > other_two && median < other_one
    };

    if comparison(beginning, middle, end) {
        left
    } else if comparison(middle, end, beginning) {
        half_index
    } else if comparison(end, beginning, middle) {
        right
    } else {
        left
    }
}

fn partition(
    list: &mut Vec<impl PartialOrd>,
    left: usize,
    right: usize,
    pivot_index: usize,
) -> usize {
    list.swap(pivot_index, right);

    let mut store_index = left;
    for i in left..right {
        if list[i] < list[right] {
            list.swap(i, store_index);
            store_index += 1
        }
    }
    list.swap(right, store_index);
    store_index
}

fn _select<T: PartialOrd>(x: &mut Vec<T>, left: usize, right: usize, k: usize) -> &T {
    if left == right {
        &x[left]
    } else {
        let pivot_index = partition(x, left, right, median_of_three(&x, left, right));
        if k == pivot_index {
            &x[k]
        } else if k < pivot_index {
            _select(x, left, pivot_index - 1, k)
        } else {
            _select(x, pivot_index + 1, right, k)
        }
    }
}

fn select<T: PartialOrd>(array: &mut Vec<T>, k: usize) -> &T {
    _select(array, 0, array.len() - 1, k)
}

#[cfg(test)]
mod tests {
    use crate::{partition, select, _select};

    #[test]
    fn partition_test() {
        let mut vector = vec![1, 1, -43, 0, -1, -1, -1];
        let len = vector.len() - 1;
        let result = partition(&mut vector, 0, len, 3);
        assert_eq!(vector, vec![-43, -1, -1, -1, 0, 1, 1]);
        assert_eq!(result, 4)
    }

    #[test]
    fn select_test() {
        let mut vector = vec![3, 2, 1, 6, 5, 4, 0];
        let len = vector.len() - 1;
        for i in 1..=len {
            let result = *_select(&mut vector, 0, len, i);
            dbg!(&vector);
            assert_eq!(result, i)
        }
    }

    #[test]
    fn it_works() {
        let mut vector = vec![100, 2, 7, 1, 4, 43, 0];
        for i in 0..vector.len() {
            println!("{}", select(&mut vector, i));
            dbg!(&vector);
        }
    }
}