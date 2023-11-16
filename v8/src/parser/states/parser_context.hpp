#pragma once
#ifndef ORG_YAPLLANG_PARSER_CONTEXT_HPP
#define ORG_YAPLLANG_PARSER_CONTEXT_HPP

#include "include.hpp"
#include "parser_states.hpp"
#include "../parser.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "lexer/tokenizer/tokenizer_line.hpp"
#include "lexer/lexer_exception.hpp"
#include "../parser_exception.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

class ParserContext {
    public:
        ParserContext(const lexer::tokenizer::TokenizerLine &line, std::vector<ParserState>& stateStack, std::vector<size_t> &indentation);

        void pushOutputToken(const parser::ParserToken &token);
        void push(ParserState state, const parser::ParserToken &token);
        void push(ParserState state);
        void pop(ParserState state, const parser::ParserToken &token);
        void pop(ParserState state);
        ParserState getCurrentState() const;
        const lexer::tokenizer::TokenizerLine &getCurrentLine() const;
        bool emptyState() const; 

        void indent(const std::string &whitespace);
        int maybeDedent(const std::string &whitespace);
        bool wouldDedent(const std::string &whitespace) const;
        bool wouldIndent(const std::string &whitespace) const;
        size_t getIndentLength() const;

        const std::vector<parser::ParserToken> &getOutputTokens();
        std::vector<parser::ParserToken> &mutateOutputTokens();

        std::string addContextToErrorMessage(const std::string &message) const;

        ParserException parserException(const std::string& message);
        ClosingUnopenedBlockException closingUnopenedBlockException(const parser::ParserToken& token);
        UnknownEscapeCharacterException unknownEscapeCharacterException(const parser::ParserToken& token);
        InvalidTokenInThisContextException invalidTokenInThisContextException(const parser::ParserToken& token, const states::ParserState state, const std::string &message);
        UnclosedOpenedBlockException unclosedOpenedBlockException(const std::string &message);
        lexer::LexerException lexerException(const std::string& message);
        Exception exception(const std::string& message);

    private:
        std::vector<size_t> &indentation_;
        lexer::tokenizer::TokenizerLine line_;
        std::vector<parser::ParserToken> outputTokens_;
        std::vector<ParserState>& stateStack_;
};

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_CONTEXT_HPP
