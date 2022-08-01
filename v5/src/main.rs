use std::env;
use std::process::ExitCode;

mod transpiler_frontend;
mod transpilation_job;
mod abstract_syntax_tree;

use transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};
use transpilation_job::builder::TranspilationJobBuilder;

fn run(args: &Vec<String>, output: &mut TranspilationJobOutput) {
    if args.len() != 3 {
        output.report_error(
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
                transpiler.append_output_to(output);
            }
            Err(_) => {
                builder.append_output_to(output);
            }
        }
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    let mut output = TranspilationJobOutput::create();
    run(&args, &mut output);
    if output.was_successful() {
        println!("Transpilation completed successfully.");
    } else {
        println!("Transpilation failed.");
    }
    let l = output.get_transpilation_output_len();
    for i in 0..l {
        let o = output.get_transpilation_output_message(i);
        if o.line.is_none() {
            println!("{}: {}", i, o.message);
        } else {
            let line = o.line.unwrap();
            let prefix = format!("{} [line={}]: ",  i, line.line_number);
            println!("{}{}", prefix, o.message);
            println!("{}> {}", "-".repeat(prefix.len() - 2), line.line_text);
            
        }
    }
    return output.get_exit_code();
}