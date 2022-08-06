use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;
use crate::abstract_syntax_tree::nodes::section_node::AbstractSyntaxTreeSectionNodeVisibility;
use crate::abstract_syntax_tree::nodes::callable_node::AbstractSyntaxTreeCallableNode;

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeClassFacetNode {
    pub maybe_class_facet_name: Option<String>,
    pub maybe_section_visibility: Option<AbstractSyntaxTreeSectionNodeVisibility>,
    pub maybe_prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub maybe_suffix_comment: Option<String>,
    pub callable_nodes: Vec<AbstractSyntaxTreeCallableNode>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeClassFacetNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::ClassFacetNode;
    }

    fn as_class_facet_node(&self) -> Option<&AbstractSyntaxTreeClassFacetNode> {
        return Some(&self);
    }
    
}
