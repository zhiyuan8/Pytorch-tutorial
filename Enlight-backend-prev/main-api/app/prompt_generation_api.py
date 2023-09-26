from app import app
from flask import request, jsonify
from app.mongo_client import MongoClient, parameters
import requests
from app.cloud_storage import remove_model
import os
from langchain.llms import OpenAI

client = MongoClient().client
db = MongoClient().db

os.environ["OPENAI_API_KEY"] = parameters["OPENAI_API_KEY"]

# load model
llm = OpenAI(model_name="text-davinci-003", max_tokens=800, temperature=0)

def generate_prompt(query):
    from langchain import PromptTemplate
    prompt_generation_template = """
    Generate 10 product photo ideas for a serum bottle, also the ideas should not have person in it.
    1. A photo of a serum bottle in a spa setting, surrounded by candles and rose petals, high resolution, photographic style.
    2. A photo of a serum bottle in a laboratory setting, surrounded by scientific equipment, high resolution, photographic style.
    3. A photo of a serum bottle in a garden setting, surrounded by lush greenery and flowers, high resolution, photographic style.
    4. A photo of a serum bottle on a vanity, with various skincare products in the background, high resolution, photographic style.
    5. A photo of a serum bottle in a gym setting, with various workout equipment in the background, high resolution, photographic style.
    6. A photo of a serum bottle on a beach, with the ocean and sandy beach in the background, high resolution, photographic style.
    7. A photo of a serum bottle in a bedroom setting, with a comfortable bed and soft lighting in the background, high resolution, photographic style.
    8. A photo of a serum bottle in a kitchen setting, with a variety of healthy food and drink options in the background, high resolution, photographic style.
    9. A photo of a serum bottle in a fashion setting, with high-end clothing and accessories in the background, high resolution, photographic style.
    10. A photo of a serum bottle in a beauty salon setting, with various styling tools and products in the background, high resolution, photographic style.

    =====
    Generate 10 product photo ideas for a face moisturizer, also the ideas should not have person in it.
    1. A photo of a face moisturizer in a spa setting, surrounded by candles and rose petals, high resolution, photographic style.
    2. A photo of a face moisturizer in a laboratory setting, surrounded by scientific equipment, high resolution, photographic style.
    3. A photo of a face moisturizer in a garden setting, surrounded by lush greenery and flowers, high resolution, photographic style.
    4. A photo of a face moisturizer on a vanity, with various skincare products in the background, high resolution, photographic style.
    5. A photo of a face moisturizer in a gym setting, with various workout equipment in the background, high resolution, photographic style.
    6. A photo of a face moisturizer on a beach, with the ocean and sandy beach in the background, high resolution, photographic style.
    7. A photo of a face moisturizer in a bedroom setting, with a comfortable bed and soft lighting in the background, high resolution, photographic style.
    8. A photo of a face moisturizer in a kitchen setting, with a variety of healthy food and drink options in the background, high resolution, photographic style.
    9. A photo of a face moisturizer in a fashion setting, with high-end clothing and accessories in the background, high resolution, photographic style.
    10. A photo of a face moisturizer in a beauty salon setting, with various styling tools and products in the background, high resolution, photographic style.

    =====
    Generate 10 ideas for a watershoe, also the ideas should not have person in it.
    1. A photo of a water shoe in a river or lake setting, surrounded by lush greenery and rocks, high resolution, photographic style.
    2. A photo of a water shoe on a dock or pier, with a boat in the background, high resolution, photographic style.
    3. A photo of a water shoe in a swimming pool setting, surrounded by tiles and water features, high resolution, photographic style.
    4. A photo of a water shoe in a beach setting, surrounded by sand and ocean waves, high resolution, photographic style.
    5. A photo of a water shoe on a river bank, surrounded by plants and wildlife, high resolution, photographic style.
    6. A photo of a water shoe in a kayaking or canoeing setting, surrounded by calm water and natural scenery, high resolution, photographic style.
    7. A photo of a water shoe in a waterfall or spring setting, surrounded by mist and greenery, high resolution, photographic style.
    8. A photo of a water shoe in a rafting or tubing setting, surrounded by rapids and riverbanks, high resolution, photographic style.
    9. A photo of a water shoe in a water park setting, surrounded by slides and water attractions, high resolution, photographic style.
    10. A photo of a water shoe in a fishing or boating setting, surrounded by fishing gear and a boat, high resolution, photographic style.

    =====
    Generate 10 ideas for a camping tent, also the ideas should not have person in it.
    1. A photo of a camping tent in a forest setting, surrounded by tall trees and natural foliage, high resolution, photographic style.
    2. A photo of a camping tent on a mountainside, surrounded by rugged terrain and snow-capped peaks, high resolution, photographic style.
    3. A photo of a camping tent by a lake or river, surrounded by natural scenery and wildlife, high resolution, photographic style.
    4. A photo of a camping tent on a beach, surrounded by sand and ocean waves, high resolution, photographic style.
    5. A photo of a camping tent in a desert setting, surrounded by sand dunes and cacti, high resolution, photographic style.
    6. A photo of a camping tent in a meadow or field, surrounded by tall grass and wildflowers, high resolution, photographic style.
    7. A photo of a camping tent in a snowy setting, surrounded by snow-covered trees and frozen landscapes, high resolution, photographic style.
    8. A photo of a camping tent in a national park or wilderness setting, surrounded by natural landmarks and wildlife, high resolution, photographic style.
    9. A photo of a camping tent in a backyard or garden setting, surrounded by flowers and greenery, high resolution, photographic style.
    10. A photo of a camping tent in a urban setting, surrounded by skyscrapers and city lights, high resolution, photographic style.

    =====
    Generate 10 ideas for a hiking bag, also the ideas should not have person in it.
    1. A photo of a hiking bag on a mountain trail, surrounded by rugged terrain and snow-capped peaks, high resolution, photographic style.
    2. A photo of a hiking bag in a forest setting, surrounded by tall trees and natural foliage, high resolution, photographic style.
    3. A photo of a hiking bag on a beach, surrounded by sand and ocean waves, high resolution, photographic style.
    4. A photo of a hiking bag by a lake or river, surrounded by natural scenery and wildlife, high resolution, photographic style.
    5. A photo of a hiking bag on a snowy mountain trail, surrounded by snow-covered trees and frozen landscapes, high resolution, photographic style.
    6. A photo of a hiking bag in a desert setting, surrounded by sand dunes and cacti, high resolution, photographic style.
    7. A photo of a hiking bag in a meadow or field, surrounded by tall grass and wildflowers, high resolution, photographic style.
    8. A photo of a hiking bag in a national park or wilderness setting, surrounded by natural landmarks and wildlife, high resolution, photographic style.
    9. A photo of a hiking bag in a backyard or garden setting, surrounded by flowers and greenery, high resolution, photographic style.
    10. A photo of a hiking bag in an urban setting, surrounded by skyscrapers and city lights, high resolution, photographic style.

    =====
    Generate 10 ideas for a jelly drink, also the ideas should not have person in it.
    1. A photo of a jelly drink in a park, surrounded by lush greenery and natural landscapes, high resolution, photographic style.
    2. A photo of a jelly drink in a beach setting, surrounded by sand and ocean waves, high resolution, photographic style.
    3. A photo of a jelly drink in a pool, surrounded by blue water and poolside accessories, high resolution, photographic style.
    4. A photo of a jelly drink on a city sidewalk, surrounded by tall buildings and urban landscapes, high resolution, photographic style.
    5. A photo of a jelly drink at a amusement park, surrounded by colorful rides and attractions, high resolution, photographic style.
    6. A photo of a jelly drink in a garden, surrounded by vibrant flowers and greenery, high resolution, photographic style.
    7. A photo of a jelly drink in a forest, surrounded by tall trees and natural landscapes, high resolution, photographic style.
    8. A photo of a jelly drink at a picnic, surrounded by picnic blanket and accessories, high resolution, photographic style.
    9. A photo of a jelly drink at a food festival, surrounded by a variety of foods and colorful decorations, high resolution, photographic style.
    10. A photo of a jelly drink in a home kitchen, surrounded by appliances and ingredients, high resolution, photographic style.

    =====
    Generate 10 ideas for a watch, also the ideas should not have person in it.
    1. A photo of a watch on a sleek and modern desk, surrounded by office equipment and technology, high resolution, photographic style.
    2. A photo of a watch on a wooden table, surrounded by natural elements such as stones and plants, high resolution, photographic style.
    3. A photo of a watch in a display case, surrounded by other luxury watches and jewelry, high resolution, photographic style.
    4. A photo of a watch on a car dashboard, surrounded by car accessories and the car's interior, high resolution, photographic style.
    5. A photo of a watch on a book, surrounded by a variety of literature and other reading materials, high resolution, photographic style.
    6. A photo of a watch on a nightstand, surrounded by other bedroom accessories such as a lamp and alarm clock, high resolution, photographic style.
    7. A photo of a watch on a city street, surrounded by tall buildings and urban landscapes, high resolution, photographic style.
    8. A photo of a watch on a nature trail, surrounded by trees and natural landscapes, high resolution, photographic style.
    9. A photo of a watch in a workshop, surrounded by tools and other equipment, high resolution, photographic style.
    10. A photo of a watch on a airplane tray table, surrounded by airplane essentials such as headphones and a book, high resolution, photographic style.

    ===== 
    Generate 10 ideas for a perfume, also the ideas should not have person in it.
    1. A photo of a perfume bottle on a vanity, surrounded by other beauty products and accessories, high resolution, photographic style.
    2. A photo of a perfume bottle on a windowsill, surrounded by natural light and greenery, high resolution, photographic style.
    3. A photo of a perfume bottle on a shelf, surrounded by other perfumes and luxury products, high resolution, photographic style.
    4. A photo of a perfume bottle on a table in a luxurious setting, such as a hotel room or a spa, high resolution, photographic style.
    5. A photo of a perfume bottle on a dresser, surrounded by other personal items such as jewelry and trinkets, high resolution, photographic style.
    6. A photo of a perfume bottle on a bookshelf, surrounded by literature and other reading materials, high resolution, photographic style.
    7. A photo of a perfume bottle on a white background, to focus on the design and details of the bottle, high resolution, photographic style.
    8. A photo of a perfume bottle on a table in a elegant living room, surrounded by high-end decor, high resolution, photographic style.
    9. A photo of a perfume bottle on a table in a stylish boutique, surrounded by other fashion and beauty products, high resolution, photographic style.
    10. A photo of a perfume bottle on a table in a romantic setting, such as a candlelit dinner or a rooftop terrace, high resolution, photographic style.

    =====
    Generate 10 ideas for a boot, also the ideas should not have person in it.
    1. A photo of a boot on a snowy mountain trail, surrounded by snow-covered trees and rugged terrain, high resolution, photographic style.
    2. A photo of a boot in a muddy field, surrounded by tall grass and wildflowers, high resolution, photographic style.
    3. A photo of a boot in a city setting, surrounded by skyscrapers and concrete, high resolution, photographic style.
    4. A photo of a boot in a forest setting, surrounded by tall trees and natural foliage, high resolution, photographic style.
    5. A photo of a boot on a rocky beach, surrounded by waves and rugged coastline, high resolution, photographic style.
    6. A photo of a boot in a desert setting, surrounded by sand dunes and cacti, high resolution, photographic style.
    7. A photo of a boot in a farm or ranch setting, surrounded by fields and livestock, high resolution, photographic style.
    8. A photo of a boot in a construction or industrial setting, surrounded by machinery and tools, high resolution, photographic style.
    9. A photo of a boot in a suburban setting, surrounded by houses and lawns, high resolution, photographic style.
    10. A photo of a boot in a historical or heritage setting, surrounded by old buildings or monuments, high resolution, photographic style.

    =====
    Generate 10 ideas for a shoe, also the ideas should not have person in it.
    1. A photo of a shoe on a city sidewalk, with tall buildings in the background, high resolution, photographic style.
    2. A photo of a shoe on a hiking trail, with mountains in the background, high resolution, photographic style.
    3. A photo of a shoe on a wooden dock, with a lake or river in the background, high resolution, photographic style.
    4. A photo of a shoe in a park, with lush greenery and trees in the background, high resolution, photographic style.
    5. A photo of a shoe on a basketball court, with a basketball hoop in the background, high resolution, photographic style.
    6. A photo of a shoe on a running track, with a finish line in the background, high resolution, photographic style.
    7. A photo of a shoe on a golf course, with a golfer in the background, high resolution, photographic style.
    8. A photo of a shoe in a gym, with workout equipment in the background, high resolution, photographic style.
    9. A photo of a shoe in a concert venue, with a band or musicians in the background, high resolution, photographic style.
    10. A photo of a shoe in a coffee shop or bookstore, with books or coffee cups in the background, high resolution, photographic style.

    =====
    Generate 10 ideas for a {query}, also the ideas should not have person in it.
    """

    prompt_generation_prompt_template = PromptTemplate(    
        input_variables=["query"],
        template=prompt_generation_template
    )

    prompt_generation_prompt = prompt_generation_prompt_template\
                               .format(query=query)

    # run the prompt
    result = llm(prompt=prompt_generation_prompt)

    # parse the result, each line is a prompt
    result = result.splitlines()
    result_final = []
    for i in range(len(result)):
        # remove the prompt number
        try:
            result[i] = result[i].split(" ", 1)[1]
            if query in result[i]:
                result_final.append(result[i])
        except:
            pass

    return result_final
