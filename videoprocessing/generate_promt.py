from openai import OpenAI

client = OpenAI()

#choose between gpt-3.5-turbo and gpt-4.0
MODEL = "gpt-3.5-turbo"

def generate_answer(input_string, output_file, nr):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "For the next questions I want you to follow this scheme: "
                "1) You will receive a slide from a lecture and some text which is spoken "
                "while the slide is shown."
                "If no slide is provided, only use text"
                "2) You will identify the topic that is being discussed"
                "3) You will write a summary of the topic using text, slide and additional "
                "information you can find from other sources."
                "The summary should contain all the information and not skip any information."
                "Structure the summary in bullet points, while not shortening it!"
                "4) Provide questions one should be able to answer after reading the summary"},
            {"role": "user", "content": f"{input_string}"}
        ]
    )
    answer = response.choices[0].message.content + "\n"
    f = open(output_file, 'a')
    f.write(f"Answer: {nr}\n")
    f.write(answer)
    f.close()
    print(response.choices[0].message.content)


#generate_answer("text", "textoutput.txt" ,0)
