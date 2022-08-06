pub mod builder;
pub mod output;

use std::io::BufRead;
use std::fs;

use crate::transpilation_job::output::{
    TranspilationJobOutput,
    TranspilationJobOutputErrorCode
};

use crate::transpiler_frontend::context::TranspilerFrontendContext;
use crate::transpiler_frontend::line::TranspilerFrontendLine;
use crate::transpiler_frontend::parsers::file_parser::TranspilerFrontendFileParser;

pub struct TranspilationJob {
    abs_source_filename: String,
    abs_target_dirname: String,
}

impl TranspilationJob {

    pub fn create(
        abs_source_filename: &String,
        abs_target_dirname: &String
    ) -> TranspilationJob {
        return TranspilationJob {
            abs_source_filename: abs_source_filename.clone(),
            abs_target_dirname: abs_target_dirname.clone()
        }
    }

    pub fn transpile(&mut self) {
        let file_result = fs::File::open(&self.abs_source_filename);
        if file_result.is_err() {
            TranspilationJobOutput::report_error(
                format!("ERROR: failed to open file ({:?}) for reading:", self.abs_source_filename),
                TranspilationJobOutputErrorCode::TranspilationJobFailedToOpenSourceFile
            )
        }
        else {
            let mut context = TranspilerFrontendContext::create();
            context.push(TranspilerFrontendFileParser::create());
            let buf_reader = std::io::BufReader::new(file_result.unwrap());
            let mut line_number:usize = 1;
            for line in buf_reader.lines() {
                if line.is_err() {
                    TranspilationJobOutput::report_error(
                        format!("ERROR: failed to read line #{} from {:?}", line_number, self.abs_source_filename),
                        TranspilationJobOutputErrorCode::TranspilationJobFailedToReadSourceLine
                    );
                    break;
                }
                let actual_line = line.unwrap();
                println!("transpiling line {}: {:?}", line_number, actual_line);
                // replace all tabs with 4 spaces
                let line_of_text_without_tabs = &actual_line.replace("\t", "    ");
                let transpiler_line = TranspilerFrontendLine::create(line_number, &line_of_text_without_tabs);
                self.transpile_input_line(&mut context, &transpiler_line);
                line_number += 1;
            }
            while !context.is_empty() {
                let mut current = context.pop();
                current.end_of_file(&mut context);
                context.push(current);
                context.handle_pending_requests();
            }
        }
    }

    fn transpile_input_line(&mut self, context: &mut TranspilerFrontendContext, input_line: &TranspilerFrontendLine) {
        let mut current = context.pop();
        current.append_line(context, input_line);
        context.push(current);
        let popped_line = context.handle_pending_requests();
        if !popped_line.is_none() {
            self.transpile_input_line(context, popped_line.as_ref().unwrap());
        }
    }
}
