use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeCallableNode {
    pub callable_type: String,
    pub maybe_callable_name: Option<String>,
    pub maybe_prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub maybe_suffix_comment: Option<String>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeCallableNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::CallableNode;
    }

    fn as_callable_node(&self) -> Option<&AbstractSyntaxTreeCallableNode> {
        return Some(&self);
    }
    
}
