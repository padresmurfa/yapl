use std::env;
use std::process::ExitCode;
#[macro_use]
extern crate lazy_static;

mod transpiler_frontend;
mod transpilation_job;
mod abstract_syntax_tree;

use transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use transpilation_job::builder::TranspilationJobBuilder;

fn run(args: &Vec<String>) {
    if args.len() != 3 {
        TranspilationJobOutput::report_error(
            format!("ERROR: Expected 2 arguments, got {}\nUsage: yapl <source-file> <target-dir>", args.len()),
            TranspilationJobOutputErrorCode::MainMissingCommandLineArguments
        );
    } else {
        let mut builder = TranspilationJobBuilder::create().
            set_source_filename(&args[1]).
            set_target_dirname(&args[2]);
        let build_result = builder.build();
        match build_result {
            Ok(_) => {
                let mut transpiler = build_result.unwrap();
                transpiler.transpile();
            }
            Err(_) => {
            }
        }
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    run(&args);
    TranspilationJobOutput::print_output();
    return TranspilationJobOutput::get_exit_code();
}