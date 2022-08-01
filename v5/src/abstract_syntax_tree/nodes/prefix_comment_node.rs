use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};

#[derive(Debug, Clone)]
pub enum AbstractSyntaxTreePrefixCommentNodeValue {
    EmptyLine,
    HorizontalRule,
    Comment(String)
}

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreePrefixCommentNode {
    pub comment_lines: Vec<AbstractSyntaxTreePrefixCommentNodeValue>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreePrefixCommentNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::PrefixCommentNode;
    }

    fn as_prefix_comment_node(&self) -> Option<&AbstractSyntaxTreePrefixCommentNode> {
        return Some(&self);
    }
    
}
