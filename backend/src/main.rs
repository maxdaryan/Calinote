mod crypto;
mod store;

use std::io::{self, Read};
use std::path::Path;
use serde::Deserialize;
use serde_json::Value;

// ── Macro helper ─────────────────────────────────────────────────────────────

macro_rules! unwrap_or {
    ($opt:expr, $msg:expr) => {
        match $opt {
            Some(v) => v,
            None    => return err($msg),
        }
    };
}

// ── Request / Response types ────────────────────────────────────────────────

#[derive(Deserialize)]
struct Request {
    cmd: String,
    // save
    path:     Option<String>,
    title:    Option<String>,
    body:     Option<String>,
    password: Option<String>,
    // list
    dir:      Option<String>,
}

fn ok(extra: Value) -> Value {
    let mut m = serde_json::Map::new();
    m.insert("ok".into(), Value::Bool(true));
    if let Value::Object(map) = extra {
        m.extend(map);
    }
    Value::Object(m)
}

fn err(msg: &str) -> Value {
    serde_json::json!({ "ok": false, "error": msg })
}

// ── Dispatch ─────────────────────────────────────────────────────────────────

fn handle(req: Request) -> Value {
    match req.cmd.as_str() {
        // ── save ───────────────────────────────────────────────────────────
        "save" => {
            let path     = unwrap_or!(req.path,     "Missing 'path'");
            let title    = unwrap_or!(req.title,    "Missing 'title'");
            let body     = unwrap_or!(req.body,     "Missing 'body'");
            let password = unwrap_or!(req.password, "Missing 'password'");

            match store::save_note(Path::new(&path), &title, &body, &password) {
                Ok(())   => ok(serde_json::json!({})),
                Err(e)   => err(&e),
            }
        }

        // ── load ───────────────────────────────────────────────────────────
        "load" => {
            let path     = unwrap_or!(req.path,     "Missing 'path'");
            let password = unwrap_or!(req.password, "Missing 'password'");

            match store::load_note(Path::new(&path), &password) {
                Ok((title, body)) => ok(serde_json::json!({ "title": title, "body": body })),
                Err(e)            => err(&e),
            }
        }

        // ── list ───────────────────────────────────────────────────────────
        "list" => {
            let dir = unwrap_or!(req.dir, "Missing 'dir'");

            match store::list_notes(Path::new(&dir)) {
                Ok(notes) => ok(serde_json::json!({ "notes": notes })),
                Err(e)    => err(&e),
            }
        }

        // ── delete ─────────────────────────────────────────────────────────
        "delete" => {
            let path = unwrap_or!(req.path, "Missing 'path'");

            match store::delete_note(Path::new(&path)) {
                Ok(())  => ok(serde_json::json!({})),
                Err(e)  => err(&e),
            }
        }

        other => err(&format!("Unknown command: '{other}'")),
    }
}

// ── Main ──────────────────────────────────────────────────────────────────────

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read stdin");

    let response = match serde_json::from_str::<Request>(&input) {
        Ok(req)  => handle(req),
        Err(e)   => err(&format!("JSON parse error: {e}")),
    };

    println!("{}", serde_json::to_string(&response).unwrap());
}
