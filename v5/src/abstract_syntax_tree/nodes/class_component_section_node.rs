use crate::abstract_syntax_tree::nodes::{
    AbstractSyntaxTreeNodeIdentifier,
    AbstractSyntaxTreeNode
};
use crate::abstract_syntax_tree::nodes::prefix_comment_node::AbstractSyntaxTreePrefixCommentNode;
use crate::abstract_syntax_tree::nodes::section_node::AbstractSyntaxTreeSectionNodeVisibility;

#[derive(Debug, Clone)]
pub struct AbstractSyntaxTreeClassComponentSectionNode {
    pub class_component_section_name: String,
    pub maybe_section_visibility: Option<AbstractSyntaxTreeSectionNodeVisibility>,
    pub maybe_prefix_comment: Option<AbstractSyntaxTreePrefixCommentNode>,
    pub maybe_suffix_comment: Option<String>
}

impl AbstractSyntaxTreeNode for AbstractSyntaxTreeClassComponentSectionNode {
    fn get_node_type_identifier(&self) -> AbstractSyntaxTreeNodeIdentifier {
        return AbstractSyntaxTreeNodeIdentifier::ClassComponentSectionNode;
    }

    fn as_class_component_section_node(&self) -> Option<&AbstractSyntaxTreeClassComponentSectionNode> {
        return Some(&self);
    }
    
}
