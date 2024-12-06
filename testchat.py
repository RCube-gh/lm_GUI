import sys
from gpt4all import GPT4All
model=GPT4All('orca-mini-3b-gguf2-q4_0.gguf')
while True:
    input_text=input('You> ')
    if input_text=='exit' or input_text=='quit':
        break
    else:
        print('generating response...',end='')
        sys.stdout.flush()
        output=model.generate(input_text,max_tokens=100)
        sys.stdout.write("\033[2K\033[G")
        sys.stdout.flush()
        print('AI>',output)


