Hangman_stages = [
#Stage 0 (No Wrong Guess)
    """
    +=====+
    |     |
    |
    |
    |
    |
===========   
    """,
#Stage 1 (First Worng Guess)
    r"""
    +=====+
    |     |
    |     O
    |
    |
    |
 ============    
    """,
#Stage 2 (Second Wrong Guess)
    r""" 
    +=====+
    |     |
    |     O
    |     |
    |
    |
 ============  
    """,
#Stage 3 (Third Wrong Guess)
    r"""
    +=====+
    |     |
    |     O
    |    /| 
    |
    |
 ============  
    """,
#Stage 4 (Forth Wrong Guess)
    r""" 
    +=====+
    |     |
    |     O
    |    /|\ 
    |
    |
 ============  
    """,
#Stage 5 (Fifth Wrong Guess)
    r""" 
    +=====+
    |     |
    |     O
    |    /|\ 
    |    /
    |
 =============  
    """,
#Stage 6 (Sixth Wrong Guess)
    r"""
    +=====+
    |     |
    |     O
    |    /|\ 
    |    / \
    |
 =============  
    """
]

#Returns the ASCII art string for the current Wrong guess number
def get_hangman_stage(wrong_guess: int) -> str:
    if 0<= wrong_guess <len(Hangman_stages):
        return Hangman_stages[wrong_guess]
    else:
        return Hangman_stages[-1]
    
   