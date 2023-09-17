pub fn merge_sort(a: &Vec<i32>) -> Vec<i32> {
    if a.len() < 2 {
        a.to_vec()
    } else {
        let mid = a.len() / 2;
        let l = merge_sort(&a[0..mid].to_vec());
        let r = merge_sort(&a[mid..].to_vec());
        let merged = merge(&l, &r);

        merged
    }
}

fn merge(l: &Vec<i32>, r: &Vec<i32>) -> Vec<i32> {
    let mut i = 0;
    let mut j = 0;
    let mut g: Vec<i32> = Vec::new();

    while i < l.len() && j < r.len() {
        if l[i] < r[j] {
            g.push(l[i]);
            i += 1;
        } else {
            g.push(r[j]);
            j += 1;
        }
    }

    if i < l.len() {
        while i < l.len() {
            g.push(l[i]);
            i += 1;
        }
    }

    if j < r.len() {
        while j < r.len() {
            g.push(r[j]);
            j += 1;
        }
    }

    g
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn single_len_vec() {
        let mut unsorted: Vec<i32> = vec![1];
        let sorted: Vec<i32> = merge_sort(&unsorted).to_vec();
        assert_eq!(sorted, vec![1])
    }

    #[test]
    fn success() {
        let mut unsorted: Vec<i32> = vec![5,2,3,4,1,6];
        let sorted: Vec<i32> = merge_sort(&unsorted).to_vec();
        assert_eq!(sorted, vec![1,2,3,4,5,6])
    }
}