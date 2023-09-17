use rand::Rng;

fn choose_pivot_idx(len: usize) -> isize {
    let mut rng = rand::thread_rng();
    rng.gen_range(0..len as isize)
}

fn partition<T: Ord>(arr: &mut [T], l: isize, r: isize) -> isize {
    let pivot = r;
    let mut i: isize = l as isize - 1;

    for j in l..=r - 1 {
        if arr[j as usize] <= arr[pivot as usize] {
            i += 1;
            arr.swap(i as usize, j as usize);
        }
    }

    arr.swap((i + 1) as usize, pivot as usize);

    i + 1
}

pub fn quick_sort<T: Ord>(arr: &mut [T]) {
    let len = arr.len();
    _quick_sort(arr, 0, (len - 1) as isize);
}

fn _quick_sort<T: Ord>(arr: &mut [T], l: isize, r: isize) {
    if l <= r {
        let partition_idx = partition(arr, 0, r);
        _quick_sort(arr, l, partition_idx - 1);
        _quick_sort(arr, partition_idx + 1, r);
    }
}

fn main() {
    let mut numbers: [i32; 10] = [4, 65, 2, -31, 0, 99, 2, 83, 782, 1];
    println!("Before: {:?}", numbers);
    quick_sort(&mut numbers);
    println!("After:  {:?}\n", numbers);
}

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn test_choose_partition() {
//         let t = vec![1, 2, 3, 4, 5];
//         let p = choose_partition(&t);
//         assert!(t[p] > 0);
//     }

//     #[test]
//     fn test_partition() {
//         let mut t = vec![3, 2, 1, 5, 6];
//         partition(&mut t, 0, 4);
//         assert_eq!(t, [1, 2, 3, 5, 6])
//     }
// }
