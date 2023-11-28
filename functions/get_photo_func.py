import os


async def get_user_photo(bot, user_id, dir_name):
    photo = await bot.get_user_profile_photos(user_id)
    if photo.total_count != 0:
        file_id = photo.photos[0][-1].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, os.path.join(dir_name, "user_photo.png"))
        return os.path.join(dir_name, "user_photo.png")


async def get_photo(bot, file_id, dir_name, img_name):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, os.path.join(dir_name, f"{img_name}.png"))
    return os.path.join(dir_name, f"{img_name}.png")
