use std::io;
use std::collections::HashMap;

fn main() {
    let mut raw_html = String::new();
    let dom_map = HashMap::new();
    let attrs_map = HashMap::new();

    println!("Please paste raw HTML");
    io::stdin()
        .read_line(&mut raw_html)
        .expect("Invalid HTML structure");

    'parse_html : loop {

    }
}


fn lexer() {

}