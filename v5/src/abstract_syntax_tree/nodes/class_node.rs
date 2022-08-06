use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeClassNode {
    pub maybe_class_name: Option<String>,
    pub maybe_prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub maybe_suffix_comment: Option<String>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeClassNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::ClassNode;
    }

    fn as_class_node(&self) -> Option<&AbstractSyntaxTreeClassNode> {
        return Some(&self);
    }
    
}
