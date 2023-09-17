pub fn sort_and_count(a: &Vec<i32>) -> (Vec<i32>, usize) {
    if a.len() < 2 {
        (a.to_vec(), 0)
    } else {
        let mid = a.len() / 2;
        let (l, x) = sort_and_count(&a[0..mid].to_vec());
        let (r, y) = sort_and_count(&a[mid..].to_vec());
        let (d, z) = merge_and_count(&l, &r);
        (d, x + y + z)
    }

    
}

fn merge_and_count(l: &Vec<i32>, r: &Vec<i32>) -> (Vec<i32>, usize) {
    let mut i = 0;
    let mut j = 0;
    let mut ct = 0;
    let mut g: Vec<i32> = Vec::new();

    while i < l.len() && j < r.len() {
        if l[i] < r[j] {
            g.push(l[i]);
            i += 1;
        } else {
            g.push(r[j]);
            j += 1;
            ct += l.len() - i;
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

    (g, ct)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn success() {
        let mut unsorted: Vec<i32> = vec![1, 3, 5, 2, 4, 6];
        let (vec, ct) = sort_and_count(&unsorted);
        assert_eq!(ct, 3)
    }
}