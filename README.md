# UniReference

Welcome to the UniReference program, helping you to do university referencing.

To see the files used by the program, including the list of University styles it can reference and each of their sources, navigate to:

        dist > UniReference > files

The file styles.txt contains the list of University styles the program can reference in.

The other named files contain the sources that the program can reference.

Running:
 -

To run the basic CLI executable to run the program, execute:

        dist > UniReference > UniReference.exe

When running the program, some tips:

 - Type "EXIT" at any time to exit the program
 - When copying to the clipboard, the program cannot copy the italics format, please keep note of what parts need to be in italics
 - If nothing is required for an input, you can press enter, but it is likely the "," or another character will appear in the reference, please remove this when it is pasted.

Creating new styles/sources:
 -

To create a new style, include the new name in the styles.txt file on the line below the current. Then create a new .txt file with THE SAME NAME as the one you entered in the styles.txt file.

To create a new source, go inside the file of the style you want to put the source in. The format that you should use is:

        Name of source, name or organisation?, online?: [reference source] Citation: ([citation source])

The key characters:

 - "< >" - user input - anything between these characters are classed as a user input, there is a list inside of the python code of common inputs like last name, dates etc. However, using an unknown word is allowed and will print whatever is between the < > to the user for input
 - "^ ^" - italics markers - puts anything between the characters in italics, only appears in the program, copying to clipboard removes these markers
 - "~ ~" - loop markers - tells the program to loop for more inputs. Two types: "name, len" and "name". "name, len" should be used in the reference source, takes multiple inputs by outputting the name to the user to ask if they want to loop and the len tells the program how many characters to jump back (should be 1 character more than required). "name" should be used in citation to loop through already inputted values to add them.
 - "# #" - reuses an previously inputted value again, mainly for citations