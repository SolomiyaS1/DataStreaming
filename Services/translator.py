from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# hi_text = "जीवन एक चॉकलेट बॉक्स की तरह है।"
# chinese_text = "生活就像一盒巧克力。"

model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

# translate from other languages to English
def translate2english(input_text, language):

    global model, tokenizer
    tokenizer.src_lang = language
    encoded_zh = tokenizer(input_text, return_tensors="pt")
    generated_tokens = model.generate(**encoded_zh, forced_bos_token_id=tokenizer.get_lang_id("en"))
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]