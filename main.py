def create_caption(product_detail) -> str:
    price = product_detail.pop('price')
    link = product_detail.pop('Link')
    caption = ""
    for key, item in product_detail.items():
        caption += f"<b>{key}:</b> {item}" + '\n'
    if price.get('off'):
        caption += "<s><b>Old Price:</b> " + "{:,}".format(float(price.get(
            'old_price'))) + "</s> T" + '\n' + f"<b>OFF:</b> {price.get('off')}" + '\n' + "💰 <b>New Price:</b> " + "{:,}".format(
            float(price.get('new_price'))) + " T" + '\n'
    else:
        caption += "💰 <b>Price:</b> " + "{:,}".format(float(price.get('real_price'))) + " T" + '\n'
    caption += f'🔗 <b>Link:</b> {link}' + '\n'
    caption += '📞 <b>Contact:</b> +989331764376'

    return caption


def calculate_price(products_link) -> list:
    from aed_price import get_aed_price
    from scraper import get_product_details

    all_products = []
    curr_aed_price = get_aed_price()
    for product_link in products_link:
        temp_product = get_product_details(product_link)

        if temp_product['price'].get('old_price'):
            temp_product['price']['old_price'] = (float(temp_product['price']['old_price']) + (
                    float(temp_product['price']['old_price']) * 20) / 100) * curr_aed_price
            temp_product['price']['new_price'] = (float(temp_product['price']['new_price']) + (
                    float(temp_product['price']['new_price']) * 20) / 100) * curr_aed_price
        else:
            temp_product['price']['real_price'] = (float(temp_product['price']['real_price']) + (
                    float(temp_product['price']['real_price']) * 20) / 100) * curr_aed_price
        all_products.append(temp_product)
    return all_products


if __name__ == '__main__':
    from scraper import (find_products)
    from time import sleep
    from tg_bot import create_connection
    from telegram import InputMediaPhoto
    from telegram.error import (BadRequest, RetryAfter, TimedOut)
    import re

    all_products_link = []
    for i in range(1, 6):
        all_products_link.extend(find_products(i))
    all_products_detail = calculate_price(all_products_link)

    updater = create_connection()
    counter = 0
    for product in all_products_detail:
        images = [InputMediaPhoto(media=image) for image in product.pop('images')]
        text = create_caption(product)
        successful, successful_1, successful_2 = False, False, False
        MAX_RETRY = 4
        retry = 0
        if len(text) > 1024:
            while not successful_1 or not successful_2 and retry != MAX_RETRY:
                try:
                    if not successful_1:
                        updater.bot.send_media_group(chat_id='CHANNEL-NAME', media=images)
                        successful_1 = True
                    if not successful_2:
                        updater.bot.send_message(chat_id='CHANNEL-NAME', text=text[0:4096], parse_mode='html', timeout=15)
                        successful_2 = True
                        counter += 1
                except BadRequest as e:
                    print(e.message)
                    successful_1, successful_2 = True, True
                except TimedOut as e:
                    print(e.message)
                    retry += 1
                except RetryAfter as e:
                    print(e.message)
                    retry += 1
                    sleep(int(re.search(r"\d+", e.message).group()))
        else:
            while not successful and retry != MAX_RETRY:
                try:
                    images[0].caption = text
                    images[0].parse_mode = 'html'
                    updater.bot.send_media_group(chat_id='CHANNEL-NAME', media=images)
                    successful = True
                    counter += 1
                except BadRequest as e:
                    print(e.message)
                    successful = True
                except TimedOut as e:
                    print(e.message)
                    retry += 1
                except RetryAfter as e:
                    print(e.message)
                    retry += 1
                    sleep(int(re.search(r"\d+", e.message).group()))
    print(f"counter is {counter}")
