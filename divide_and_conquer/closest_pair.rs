use std::fs::read_to_string;
// use std::io::{self, BufRead};
// use std::path::Path;
use std::str::FromStr;
use std::fmt;

#[derive(Clone, Copy, Debug, PartialEq, PartialOrd)]
struct Point {
    x: i32,
    y: i32,
}
    
#[derive(Debug, PartialEq, Eq)]
struct ParsePointError;

impl fmt::Display for ParsePointError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "error parsing point")
    }
}

impl FromStr for Point {
    type Err = ParsePointError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (x, y) = s
            .split_once(',')
            .ok_or(ParsePointError)?;

        let x_fromstr = x.parse::<i32>().map_err(|_| ParsePointError)?;
        let y_fromstr = y.parse::<i32>().map_err(|_| ParsePointError)?;

        Ok(Point {x: x_fromstr, y: y_fromstr})
    }
}

impl Point {
    fn lt(&self, other: &Point, dim: i32) -> bool {
        match dim {
            0 => self.x < other.x,
            1 => self.y < other.y,
            _ => false,
        }
        // if dim == 0 {
        //     self.x < other.x
        // } else if dim == 1 {
        //     self.y < other.y
        // }
    }
}

fn main() {
    let file = include_str!("./points.txt");
    let lines = file.split("\n");
    let points: Result<Vec<Point>, ParsePointError> = lines.map(|ln| Point::from_str(ln)).collect();

    let sorted = match points {
        Ok(pts) => {
            let expected = Point {x: 100, y: 201};
            assert_eq!(pts[0], expected);

            let sorted_x = sort_points(&pts, 0).to_vec();
            let sorted_y = sort_points(&pts, 1).to_vec();
            assert_eq!(sorted_x[0], (Point {x: 1, y: 2}));
            assert_eq!(sorted_y.last(), Some(&Point {x: 100, y: 201}));
        }, 
        Err(e) => panic!("sorting broke")
    };


}

fn closest_pair(p_x: &Vec<Point>, p_y: &Vec<Point>) -> Vec<Point> {
    if p_x.len() < 3 {
        p_x.to_vec()
    }
    
    let m_x = p_x.len() / 2;
    let q = &p_x[..m_x].to_vec();
    let r = &p_x[m_x..].to_vec();
}


fn read_lines(filename: &str) -> Vec<String> {
    read_to_string(filename) 
        .unwrap()  // panic on possible file-reading errors
        .lines()  // split the string into an iterator of string slices
        .map(String::from)  // make each slice into a string
        .collect()  // gather them together into a vector
}

/// sorts points first by x and then by y
fn sort_points(pts: &Vec<Point>, dim: i32) -> Vec<Point> {
    if pts.len() < 2 {
        pts.to_vec()
    } else {
        let mid = pts.len() / 2;
        let l = sort_points(&pts[0..mid].to_vec(), dim);
        let r = sort_points(&pts[mid..].to_vec(), dim);
        _merge(&l, &r, dim)
    }   
}

fn _merge(l: &Vec<Point>, r: &Vec<Point>, dim: i32) -> Vec<Point> {
    let mut i = 0;
    let mut j = 0;
    let mut g: Vec<Point> = Vec::new();

    while i < l.len() && j < r.len() {
        if l[i].lt(&r[j], dim) {
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