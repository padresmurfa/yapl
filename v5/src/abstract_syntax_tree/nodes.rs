pub mod module_node;
pub mod prefix_comment_node;

#[derive(PartialEq)]
pub enum AbstractSyntaxTreeNodeIdentifier {
    ModuleNode,
    PrefixCommentNode
}

pub trait AbstractSyntaxTreeNode : std::fmt::Debug {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier;

    fn as_module_node(&self) -> Option<&module_node::AbstractSyntaxTreeModuleNode> { return None; }
    fn as_prefix_comment_node(&self) -> Option<&prefix_comment_node::AbstractSyntaxTreePrefixCommentNode> { return None; }
}
