use crate::transpiler_frontend::{
    TranspilerFrontend,
    line::TranspilerFrontendLine
};
use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};

#[derive(Debug)]
struct AbstractSyntaxTreeStackItem {
    indentation_level: usize,
    abstract_syntax_tree_node: Box<dyn AbstractSyntaxTreeNode>,
}

#[derive(Debug)]
pub struct TranspilerFrontendContext {
    sha256_of_input: Option<String>,
    abstract_syntax_tree_stack: Vec<AbstractSyntaxTreeStackItem>,
    transpiler_frontend_stack: Vec<Box<dyn TranspilerFrontend>>,
    push_request: Option<Box<dyn TranspilerFrontend>>,
    pop_request: Option<TranspilerFrontendLine>
}

impl TranspilerFrontendContext {
    pub fn create() -> TranspilerFrontendContext {
        return TranspilerFrontendContext {
            sha256_of_input: None,
            abstract_syntax_tree_stack: Vec::new(),
            transpiler_frontend_stack: Vec::new(),
            push_request: None,
            pop_request: None
        };
    }

    pub fn maybe_pop_abstract_syntax_tree_node(&mut self, indentation_level: usize, node_type_identifier: AbstractSyntaxTreeNodeIdentifier) -> Option<Box<dyn AbstractSyntaxTreeNode>> {
        if self.abstract_syntax_tree_stack.is_empty() {
            return None;
        }
        let tmp = self.abstract_syntax_tree_stack.pop().unwrap();
        if tmp.indentation_level == indentation_level && tmp.abstract_syntax_tree_node.get_node_type_identifier() == node_type_identifier {
            return Some(tmp.abstract_syntax_tree_node);
        } else {
            self.abstract_syntax_tree_stack.push(tmp);
            return None;
        }
    }

    pub fn push_abstract_syntax_tree_node(&mut self, indentation_level: usize, abstract_syntax_tree_node: Box<dyn AbstractSyntaxTreeNode>) {
        let stack_item = AbstractSyntaxTreeStackItem {
            indentation_level: indentation_level,
            abstract_syntax_tree_node: abstract_syntax_tree_node
        };
        self.abstract_syntax_tree_stack.push(stack_item);
    }

    pub fn push(&mut self, transpiler_frontend: Box<dyn TranspilerFrontend>) {
        self.transpiler_frontend_stack.push(transpiler_frontend);
    }

    pub fn request_push(&mut self, transpiler_frontend: Box<dyn TranspilerFrontend>) {
        if !self.push_request.is_none() {
            panic!("we should never have to request more than one push before it is processed");
        }
        self.push_request = Some(transpiler_frontend);
    }

    pub fn handle_pending_requests(&mut self) -> Option<TranspilerFrontendLine> {
        let return_value = if self.pop_request.is_none() {
            None
        } else {
            let tmp = self.pop_request.clone();
            self.pop_request = None;
            if self.transpiler_frontend_stack.is_empty() {
                // we've reached the top of the stack, no need to pass the line further up
            } else {
                let mut dying_transpiler_frontend = self.transpiler_frontend_stack.pop().unwrap();
                if !self.transpiler_frontend_stack.is_empty() {
                    let mut receiving_transpiler_frontend = self.transpiler_frontend_stack.pop().unwrap();
                    self.transpiler_frontend_stack.push(receiving_transpiler_frontend);
                } else {
                    // panic!("popping without a parent!");
                }
            }
            tmp
        };
        if !self.push_request.is_none() {
            let push_request = self.push_request.take();
            self.transpiler_frontend_stack.push(push_request.unwrap());
        }
        return return_value;
    }

    pub fn pop(&mut self) -> Box<dyn TranspilerFrontend> {
        // precond: don't call pop more often than push!
        return self.transpiler_frontend_stack.pop().unwrap();
    }

    pub fn request_pop(&mut self, line: &TranspilerFrontendLine) {
        if self.pop_request.is_none() {
            self.pop_request = Some(line.clone());
        } else if !std::ptr::eq(self.pop_request.as_ref().unwrap(), line) {
            panic!("we should never have to request more than one pop before it is processed");
        } else {
            println!("ignoring a request to pop");
        }
    }

    pub fn request_pop_due_to_end_of_file(&mut self) {
        let line = TranspilerFrontendLine {
            line_number: usize::MAX,
            line_text: "".to_string()
        };
        self.request_pop(&line);
    }

    pub fn is_empty(&self) -> bool {
        return self.transpiler_frontend_stack.is_empty();
    }

    pub fn debug_print_abstract_syntax_tree(&self) {
        for index in 0..self.abstract_syntax_tree_stack.len() {
            let node = &self.abstract_syntax_tree_stack[index];
            println!("AST NODE #{} => {:?}", 1 + index, node);
        }
    }
}
