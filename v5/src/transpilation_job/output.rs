use std::process::ExitCode;
use std::sync::Mutex;

use super::super::transpiler_frontend::line::TranspilerFrontendLine;

#[derive(Debug)]
struct TranspilationJobOutputItem {
    message: String,
    line: Option<TranspilerFrontendLine>
}

impl Clone for TranspilationJobOutputItem  {
    fn clone(&self) -> Self {
        return TranspilationJobOutputItem {
            message: self.message.clone(),
            line: self.line.clone()
        }
    }
}

#[derive(Debug, Copy, Clone)]
pub enum TranspilationJobOutputErrorCode {
    MainMissingCommandLineArguments = 1,
    BuilderInvalidSourceFile = 2,
    BuilderInvalidTargetDir = 3,
    BuilderMissingRequiredConfiguration = 4,
    TranspilationJobFailedToOpenSourceFile = 5,
    TranspilationJobFailedToReadSourceLine = 6,
    TranspilerFrontendFileParserInvalidIdentedLine = 7,
    TranspilerFrontendFileParserInvalidStartingToken = 8,
    TranspilerFrontendPrefixCommentLineJunkInHorizontalRule = 9,
    TranspilerFrontendPrefixCommentLineMissingLeadingSpace = 10,
    TranspilerFrontendSectionParserStatementMustBeTerminatedByColon = 11,
    TranspilerFrontendSectionParserInvalidIdentedLine = 12,
    TranspilerFrontendSectionParserInvalidStartingToken = 13,
    TranspilerFrontendModuleParserStatementModuleNameInvalid = 14,
    TranspilerFrontendModuleParserStatementClassNameInvalid = 15,
    TranspilerFrontendModuleParserStatementClassFacetNameInvalid = 16
}

#[derive(Debug)]
struct TranspilationJobOutputImpl {
    error_code: Option<TranspilationJobOutputErrorCode>,
    output: Vec<TranspilationJobOutputItem>
}

impl Clone for TranspilationJobOutputImpl  {
    fn clone(&self) -> Self {
        let mut cloned_output = Vec::new();
        for i in 0..self.output.len() {
            cloned_output.push(self.output[i].clone());
        }
        return TranspilationJobOutputImpl {
            error_code: self.error_code.clone(),
            output: cloned_output
        }
    }
}

impl TranspilationJobOutputImpl {

    fn was_successful(&self) -> bool {
        return self.error_code.is_none();
    }

    fn report_info(&mut self, message: String) {
        self.output.push(TranspilationJobOutputItem {
            message: message,
            line: None
        });
    }

    fn report_error(&mut self, message: String, error_code: TranspilationJobOutputErrorCode) {
        if self.error_code.is_none() {
            self.error_code = Some(error_code);
        }
        self.output.push(TranspilationJobOutputItem {
            message: message,
            line: None
        });
    }

    fn report_error_in_line(&mut self, message: String, error_code: TranspilationJobOutputErrorCode, line: &TranspilerFrontendLine) {
        if self.error_code.is_none() {
            self.error_code = Some(error_code);
        }
        self.output.push(TranspilationJobOutputItem {
            message: message,
            line: Some(line.clone())
        });
    }

    fn get_error_code(&self) -> TranspilationJobOutputErrorCode {
        return self.error_code.expect("This function should only be called if an error has occurred");
    }

    fn get_exit_code(&self) -> ExitCode {
        if self.error_code.is_none() {
            return ExitCode::from(0);
        }
        return ExitCode::from(self.error_code.unwrap() as u8);
    }
    
    fn get_transpilation_output_len(&self) -> usize {
        return self.output.len();
    }

    fn get_transpilation_output_message(&self, num: usize) -> TranspilationJobOutputItem {
        return TranspilationJobOutputItem { 
            message: self.output[num].message.clone(),
            line: self.output[num].line.clone()
        };
    }
}

lazy_static! {
    static ref singleton: Mutex<Box<TranspilationJobOutputImpl>> = {
        return Mutex::new(Box::new(TranspilationJobOutputImpl {
            error_code: None,
            output: Vec::new()
        }));
    };
}

pub struct TranspilationJobOutput {}

impl TranspilationJobOutput {

    pub fn was_successful() -> bool {
        unsafe {
            let mut o = singleton.lock().unwrap();
            return o.was_successful();
        }
    }

    pub fn report_info(message: String) {
        unsafe {
            let mut o = singleton.lock().unwrap();
            o.report_info(message);
        }
    }

    pub fn report_error(message: String, error_code: TranspilationJobOutputErrorCode) {
        unsafe {
            let mut o = singleton.lock().unwrap();
           o.report_error(message, error_code);
        }
    }

    pub fn report_error_in_line(message: String, error_code: TranspilationJobOutputErrorCode, line: &TranspilerFrontendLine) {
        unsafe {
            let mut o = singleton.lock().unwrap();
           o.report_error_in_line(message, error_code, line);
        }
    }

    pub fn get_error_code() -> TranspilationJobOutputErrorCode {
        unsafe {
            let mut o = singleton.lock().unwrap();
            return o.get_error_code();
        }
    }

    pub fn get_exit_code() -> ExitCode {
        unsafe {
            let mut o = singleton.lock().unwrap();
            return o.get_exit_code();
        }
    }
    
    pub fn print_output() {
        unsafe {
            let mut o = singleton.lock().unwrap();
            if o.was_successful() {
                println!("Transpilation completed successfully.");
            } else {
                println!("Transpilation failed.");
            }
            let l = o.get_transpilation_output_len();
            for i in 0..l {
                let message = o.get_transpilation_output_message(i);
                if message.line.is_none() {
                    println!("{}: {}", i, message.message);
                } else {
                    let line = message.line.unwrap();
                    let prefix = format!("{} [line={}]: ",  i, line.line_number);
                    println!("{}{}", prefix, message.message);
                    println!("{}> {}", "-".repeat(prefix.len() - 2), line.line_text);
                    
                }
            }
        }
    } 
}
