
{
  lex: {
    macros: {
      identifier: "[a-zA-Z0-9_]+",
    },

    rules: [
      // semantic comments
      //    must take precedence over all other things
      [`;[ a-zA-Z]*`, `yytext = yytext.slice(1, ); return 'SEMANTIC_COMMENT';`],

      // keywords
      //    must take precedence over identifiers
      [`module`,    `return 'KEYWORD_MODULE'`],

      // identifiers
      //    must be of lower precedence than keywords
      [`{identifier}(\\.{identifier})+`,    `return 'DOT_DELIMITED_IDENTIFIER'`],
      [`{identifier}`,    `return 'IDENTIFIER'`],

      [`\n\\@\\@EOF\\@\\@`, `return 'EOF_MARKER'`],

      // ------------------------------------------------
      // Indent

      [`:\\n((    )*)`,  `

        yytext = yytext.slice(2); // strip leading : and NL
        const matchedIndent = yytext.length;

        // On new block creation, we expect indent level to go up:

        if (matchedIndent < currentIndent) {
          throw new Error(
            'Bad indent: got ' + matchedIndent +
            ', expected > ' + currentIndent
          );
        }

        // Init the indent level. All the following indentations
        // should be relative to it.

        if (!indentLevel) {
          indentLevel = matchedIndent;
          // console.log("initialising the indent level to " + indentLevel)
        }

        currentIndent = matchedIndent;
        return 'INDENT';
      `],

      // ------------------------------------------------
      // Dedent/NL

      [`\\n((    )*)`,  `
        yytext = yytext.slice(1); // strip leading NL
        const matchedIndent = yytext.length;

        // console.log('digging dedent');

        // 1. Stay in the same block, skip NL.

        if (matchedIndent === currentIndent) {
          yytext = "";
          // console.log('returning NL at matchedIndent=' + matchedIndent + ", currentIndent=" + currentIndent)
          return 'NL';
        }

        // 2. Else it should be a dedent ...

        if (matchedIndent < currentIndent) {
          // console.log('returning NL and DEDENTS')

          // If we dedent on several levels, we return several
          // dedent tokens, plus 'NL' token. So dedenting from level 3
          // to level 1, may look like: ['DEDENT', 'DEDENT', 'NL']

          const dedentTokensCount = (currentIndent - matchedIndent) / indentLevel;
          const tokens = new Array(dedentTokensCount).fill('DEDENT');

          // The "fake" NL token is to make BNF grammar simpler.
          tokens.push('NL');

          currentIndent = matchedIndent;
          return tokens;
        }

        // 3. or a bad indent
        if (currentIndent !== 0) {
          throw new Error(
            'Blocks should start with ":", ' +
            'cannot increase indent not in block' +
            ", matchedIndent: " + matchedIndent +
            ", currentIndent: " + currentIndent +
            ", yytext: " + yytext
          );
        }

        // 4. or an empty line
        // console.log('got an empty line');
        yytext = "";
      `],

      [`\\s+`,    `/* skip whitespace */`],
    ],
  },

  moduleInclude: `
    /**
     * Indentation level in YAPL is mandated at 4 characters.
     */
    let indentLevel = 4;

    /**
     * Current level of indentation.
     */
    let currentIndent = 0;

    // Event handlers.

    yyparse.onParseBegin = (string, tokenizer, options) => {
      console.log('Parsing code:', string);
    };

    yyparse.onParseEnd = (parsed) => {
      // console.log('Parsed value:', JSON.stringify(parsed));
    };

    yyparse.onShift = (token) => {
      console.log('Shifting token:', token);
      return token;
    },

    yyparse.YAPLStatement = (location, id, statements) => {
      if (statements === null) {
        return { location, id };
      }
      return { type: "STATEMENT", location, id, statements };
    }
  
    yyparse.YAPLModule = (location, id) => {
      return { type: "MODULE", location, id };
    }
    `,

  bnf: {

      Program: [
        [`Statements EOF_MARKER`, `$$ = $1`],
      ]
     /**
      * List of entries, where each entry is separated by a new line.
      */
      Statements: [
        [`Statement`, `$$ = [$1]`],
        [`Statements NL Statement`, `$$ = $1; $1.push($3)`],
        [`Statements NL`, `$$ = $1;`]
      ],

      /**
      * An entry is an identifier, which may have an optional block
      * of child entries/items.
      */
      Statement: [
        [`Module`,  `$$ = $1`],
        // [`IDENTIFIER OptionalBlockOfStatements`,  `$$ = yyparse.YAPLStatement(@$, $1, $2)`],
      ],

      OptionalBlockOfStatements: [
        [`BlockOfStatements`, `$$ = $1`],
        [`ε`,                     `$$ = null`]
      ],

      BlockOfStatements: [
        [`INDENT SEMANTIC_COMMENT DEDENT`, `$$ = $2`],
        [`INDENT SEMANTIC_COMMENT Statements DEDENT`, `$$ = $2`],
        [`INDENT Statements DEDENT`, `$$ = $2`],
      ],

      Module: [
        [`KEYWORD_MODULE DOT_DELIMITED_IDENTIFIER OptionalBlockOfStatements`, `$$ = yyparse.YAPLModule(@$, $2)`]
      ],
  }

}