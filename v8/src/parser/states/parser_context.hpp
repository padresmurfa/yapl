#pragma once
#ifndef ORG_YAPLLANG_PARSER_CONTEXT_HPP
#define ORG_YAPLLANG_PARSER_CONTEXT_HPP

#include "include.hpp"
#include "parser_states.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "lexer/tokenizer/tokenizer_line.hpp"
#include "lexer/lexer_exception.hpp"
#include "../parser_exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace parser {
namespace states {

class ParserContext {
    public:
        ParserContext(const tokenizer::TokenizerLine &line, std::vector<ParserState>& stateStack, std::vector<size_t> &indentation);

        void pushOutputToken(const tokenizer::TokenizerToken &token);
        void push(ParserState state, const tokenizer::TokenizerToken &token);
        void push(ParserState state);
        void pop(ParserState state, const tokenizer::TokenizerToken &token);
        void pop(ParserState state);
        ParserState getCurrentState() const;
        const tokenizer::TokenizerLine &getCurrentLine() const;
        bool emptyState() const; 

        void indent(const std::string &whitespace);
        int maybeDedent(const std::string &whitespace);
        bool wouldDedent(const std::string &whitespace) const;
        bool wouldIndent(const std::string &whitespace) const;
        size_t getIndentLength() const;

        const std::vector<tokenizer::TokenizerToken> &getOutputTokens();
        std::vector<tokenizer::TokenizerToken> &mutateOutputTokens();

        std::string addContextToErrorMessage(const std::string &message) const;

        ParserException parserException(const std::string& message);
        ClosingUnopenedBlockException closingUnopenedBlockException(const tokenizer::TokenizerToken& token);
        UnknownEscapeCharacterException unknownEscapeCharacterException(const tokenizer::TokenizerToken& token);
        InvalidTokenInThisContextException invalidTokenInThisContextException(const tokenizer::TokenizerToken& token, const states::ParserState state, const std::string &message);
        UnclosedOpenedBlockException unclosedOpenedBlockException(const std::string &message);
        LexerException lexerException(const std::string& message);
        Exception exception(const std::string& message);

    private:
        std::vector<size_t> &indentation_;
        tokenizer::TokenizerLine line_;
        std::vector<tokenizer::TokenizerToken> outputTokens_;
        std::vector<ParserState>& stateStack_;
};

} // namespace states
} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_CONTEXT_HPP
