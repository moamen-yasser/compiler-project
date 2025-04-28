class Scanner {
    constructor() {
        this.tokens = [];
        this.keywords = new Set([
            'if', 'else', 'while', 'for', 'int', 
            'float', 'string', 'return', 'void'
        ]);
        this.operators = new Set(['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=']);
    }

    isDigit(char) {
        return /[0-9]/.test(char);
    }

    isLetter(char) {
        return /[a-zA-Z]/.test(char);
    }

    isWhitespace(char) {
        return /\s/.test(char);
    }

    scan(sourceCode) {
        this.tokens = [];
        let currentPos = 0;

        while (currentPos < sourceCode.length) {
            let char = sourceCode[currentPos];

            // Skip whitespace
            if (this.isWhitespace(char)) {
                currentPos++;
                continue;
            }

            // Identify numbers
            if (this.isDigit(char)) {
                let number = '';
                while (currentPos < sourceCode.length && this.isDigit(sourceCode[currentPos])) {
                    number += sourceCode[currentPos];
                    currentPos++;
                }
                this.tokens.push({ type: 'NUMBER', value: number });
                continue;
            }

            // Identify identifiers and keywords
            if (this.isLetter(char)) {
                let identifier = '';
                while (currentPos < sourceCode.length && 
                       (this.isLetter(sourceCode[currentPos]) || this.isDigit(sourceCode[currentPos]))) {
                    identifier += sourceCode[currentPos];
                    currentPos++;
                }
                
                const type = this.keywords.has(identifier) ? 'KEYWORD' : 'IDENTIFIER';
                this.tokens.push({ type, value: identifier });
                continue;
            }

            // Identify operators
            if (this.operators.has(char)) {
                let operator = char;
                if (currentPos + 1 < sourceCode.length) {
                    const nextChar = sourceCode[currentPos + 1];
                    const combinedOp = char + nextChar;
                    if (this.operators.has(combinedOp)) {
                        operator = combinedOp;
                        currentPos++;
                    }
                }
                this.tokens.push({ type: 'OPERATOR', value: operator });
                currentPos++;
                continue;
            }

            // Handle special characters
            if (char === '(' || char === ')' || char === '{' || char === '}' || char === ';' || char === ',') {
                this.tokens.push({ type: 'SPECIAL', value: char });
                currentPos++;
                continue;
            }

            // Unknown character
            this.tokens.push({ type: 'UNKNOWN', value: char });
            currentPos++;
        }

        return this.tokens;
    }
}

// Initialize scanner and add event listeners
document.addEventListener('DOMContentLoaded', () => {
    const scanner = new Scanner();
    const analyzeBtn = document.getElementById('analyzeBtn');
    const sourceCode = document.getElementById('sourceCode');
    const tokenOutput = document.getElementById('tokenOutput');

    analyzeBtn.addEventListener('click', () => {
        const code = sourceCode.value;
        const tokens = scanner.scan(code);
        
        // Display tokens
        tokenOutput.innerHTML = tokens.map(token => 
            `<div class="token">${token.type}: ${token.value}</div>`
        ).join('');
    });
});