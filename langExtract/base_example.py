import textwrap
import langextract as lx
import webbrowser
input_text = "古龙（1938年6月7日一1985年9月21日），原名熊耀华，籍贯江西南昌，于香港出生。"

prompt_description = "提取姓名、出生日期、逝世日期、籍贯、出生地"

examples = [
    lx.data.ExampleData(
        text="梁思成（1901年4月20日-1972年1月9日），籍贯广东新会，生于日本东京，原名梁希。",
        extractions=[
            lx.data.Extraction(extraction_class="姓名", extraction_text="梁思成"),
            lx.data.Extraction(
                extraction_class="出生日期", extraction_text="1901年4月20日"
            ),
            lx.data.Extraction(
                extraction_class="逝世日期", extraction_text="1972年1月9日"
            ),
            lx.data.Extraction(
                extraction_class="籍贯", extraction_text="广东新会"
            ),
            lx.data.Extraction(
                extraction_class="出生地", extraction_text="日本东京"
            ),
        ],
    )
]

# Text with a medication mention
# input_text = "Alice (June 7, 1938 – September 21, 1985), originally named Xiong Yaohua, was born in Nanchang, Jiangxi"

# # Define extraction prompt
# prompt_description = "print name, birth date, death date"

# # Define example data with entities in order of appearance
# examples = [
#     lx.data.ExampleData(
#         text="Jack (April 20, 1901- January 9, 1972), originally from Xinhui, Guangdong, was born in Tokyo, Japan.",
#         extractions=[
#             lx.data.Extraction(extraction_class="name", extraction_text="Jack"),
#             lx.data.Extraction(
#                 extraction_class="birth date", extraction_text="April 20, 1901"
#             ),
#             lx.data.Extraction(
#                 extraction_class="death date", extraction_text="January 9, 1972"
#             ),
#         ],
#     )
# ]
# 配置模型
model_config = lx.factory.ModelConfig(
    model_id="QwQ-32B",
    provider="OpenAILanguageModel",
    provider_kwargs={
        "base_url": "http://192.168.6.62:8000/v1",  # 这里的不能使用下面的URL，要用base_url
        "format_type": lx.data.FormatType.JSON,
        "temperature": 0.1,
        "api_key": "123",
    },
)

# 创建模型实例
model = lx.factory.create_model(model_config)

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt_description,
    examples=examples,
    model=model,
    fence_output=False,
    use_schema_constraints=False,
)

# Display entities with positions
# print(f"Input: {input_text}\n")
# print("Extracted entities:")
for entity in result.extractions:
    position_info = ""
    if entity.char_interval:
        start, end = entity.char_interval.start_pos, entity.char_interval.end_pos
        position_info = f" (pos: {start}-{end})"
    print(
        f"• {entity.extraction_class.capitalize()}: {entity.extraction_text}{position_info}"
    )

# Save and visualize the results
lx.io.save_annotated_documents(
    [result], output_name="base_example.jsonl", output_dir="."
)

# Generate the interactive visualization
html_content = lx.visualize("base_example.jsonl")
with open("base_example.html", "w", encoding="utf-8") as f:
    if hasattr(html_content, "data"):
        f.write(html_content.data)  # For Jupyter/Colab
    else:
        f.write(html_content)

print("Interactive visualization saved to base_example.html")
webbrowser.open("base_example.html")