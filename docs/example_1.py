from markdgenerator import PandocMdGenerator

generator = PandocMdGenerator()

# text elements are by default added to the default block
generator.h1("Example")
generator.paragraph("This is an example:")
generator.h2("Code")
generator.codeparagraph("pip install markdgenerator")

# since no section is defined, the default block will be printed
print(generator)