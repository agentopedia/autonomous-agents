import gradio as gr
import cohere 
import os

co = cohere.Client(
  api_key=os.getenv('api_key'), # This is your trial API key
) 

def cohere_response(msg):
  stream = co.chat_stream( 
  model='command-r-plus',
  message=msg,
  temperature=0.3,
  chat_history=[],
  prompt_truncation='AUTO',
) 
  output = ''
  for event in stream:
     if event.event_type == "text-generation":
        output += event.text
        print(event.text, end='')
  return output

def generate_prototype(problem):
  prompt_sum = f'''You are a UX designer who is an expert in generating front-end code for a given requirement from a product manager: {problem}. Follow these step-by-step instructions to create a series of mockups that form a clickable prototype:
1.Understand the Requirement: Carefully read and understand the requirement provided by the product manager.
2.Identify Personas: Identify the personas outlined in the input problem. For example, if the requirement is for an e-commerce website, personas could include:
Shopper
Seller
Administrator
3.Generate Critical User Journeys (CUJs): For each persona, generate detailed Critical User Journeys that fully capture the persona's intent. 
4.Create Screens: Based on the CUJs, create the corresponding screens. For each screen, write HTML code that includes the header with the screen number and the CUJ it caters to. Ensure each screen links to the next to form a clickable prototype.
5.Use Bootstrap and Visual Libraries: Utilize Bootstrap and other popular visual libraries to enhance the design and functionality of the mockups.
6.Avoid Placeholders: Do not use placeholders. Instead, assume real-world use cases to make the mockups useful and realistic.
7.Ensure Visual Appeal: The mockups should be visually appealing and user-friendly.
Constraints:
8.Output HTML Code Only: Generate only the HTML code for the mockups, nothing else. Do not generate commentary around descriptions of the approach followed by the assistant. 
Do not generate images or refer to image urls in the code. 
This commentary will be too distracting to include in the HTML mocks for the Gradio app.
Example
Screen 1: Searching for a product (Shopper)
html
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Screen 1: Searching for a product (Shopper)</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>Search for a Product</h1>
        <form>
            <div class="form-group">
                <label for="search">Search</label>
                <input type="text" class="form-control" id="search" placeholder="Enter product name">
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
        <a href="screen2.html" class="btn btn-link">Next: Adding a product to the cart</a>
    </div>
</body>
</html>
Screen 2: Adding a product to the cart (Shopper)
html
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Screen 2: Adding a product to the cart (Shopper)</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>Product Details</h1>
        <p>Product Name: Awesome Widget</p>
        <p>Price: $19.99</p>
        <button class="btn btn-success">Add to Cart</button>
        <a href="screen3.html" class="btn btn-link">Next: Checking out</a>
    </div>
</body>
</html>
Follow this structure for each screen and CUJ, ensuring a seamless and visually appealing user experience.'''
  response = cohere_response(prompt_sum)
  return response

# Define a function to handle form submissions (this is just a placeholder)
def handle_form(requirements):
    print(requirements)
    emp_content = generate_prototype(requirements)
    #final_html_content = extract_html(emp_content)
    return emp_content, emp_content

# Create a Gradio interface to showcase the HTML content
gr.Interface(
    fn=handle_form,
    inputs=gr.Textbox(),
    outputs=[gr.HTML(),gr.Textbox()],
    title="Prototype Planner",
    description="Generate a prototype for a given requirement",
    examples=["Generate a clickable prototype for an e-commerce site with personas: Shopper, Seller, Administrator, and CUJs like searching for products, listing products, and managing users.","Create a prototype for an online learning platform with personas: Student, Instructor, Administrator, and CUJs like browsing courses, creating courses, and managing users.","Build a prototype for a banking app with personas: Customer, Banker, Admin, and CUJs like checking account balances, managing accounts, and overseeing transactions.","Develop a prototype for a healthcare portal with personas: Patient, Doctor, Admin, and CUJs like booking appointments, managing patient records, and overseeing user activities."],
).launch()
