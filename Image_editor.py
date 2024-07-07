from PIL import Image, ImageDraw
import cv2


class ImageEditor:
    """
    Класс, описывающий основной функционал редактирования изображений
    """
    def __init__(self):
        """
        Инициализация
        """
        self.image = None
        self.image_backup = None

    def load_image(self, file_path):
        """
        Загрузка изображения
        :param file_path: Путь к файлу
        :return: None если ошибка
        """
        try:
            self.image = Image.open(file_path)
            self.image = self.image.convert("RGB")

        except Exception as e:
            print("Ошибка при загрузке изображения:", str(e))
            return None


    @staticmethod
    def load_photo():
        """
        Метод для получения изображения с веб камеры пользователя и перехода к его редактированию
        :return: Image. если ошибка
        :return: Фотография(PIL.Image.Image)

        """
        try:
            # Включаем первую камеру
            cap = cv2.VideoCapture(0)

            # "Прогреваем" камеру, чтобы снимок не был тёмным
            for i in range(10):
                cap.read()

            # Делаем снимок
            ret, frame = cap.read()

            # Освобождаем ресурсы камеры
            cap.release()

            if ret:
                # Конвертируем изображение из формата OpenCV в формат массива numpy
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Создаем объект изображения библиотеки Pillow
                pil_image = Image.fromarray(frame_rgb)

            return pil_image.convert("RGB")

        except Exception as e:
            print("Ошибка при загрузке изображения:", str(e))
            return None

    def negative_image(self):
        """
        Создание негативного изображения
        :return:
        """
        try:
            draw = ImageDraw.Draw(self.image)
            pix = self.image.load()
            for x in range(self.image.width):
                for y in range(self.image.height):
                    r = pix[x, y][0]
                    g = pix[x, y][1]
                    b = pix[x, y][2]
                    draw.point((x, y), (255 - r, 255 - g, 255 - b))
        except Exception as e:
            print(str(e))

    def decrease_brightness(self, value):
        """
        Уменьшает яркость на заданное значение
        :param value: Значение, на которое будет уменьшена яркость
        :return:
        """

        if value > 255:
            return None

        pixels = self.image.load()
        width, height = self.image.size

        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                new_pixel = tuple(max(0, channel - value) for channel in pixel)
                pixels[x, y] = new_pixel

    def draw_circle(self, center_x, center_y, radius):
        """
        Добавляет круг на изображение
        :param center_x: X-координата центра круга
        :param center_y: Y-координата центра круга
        :param radius: Радиус круга
        :return:
        """
        draw = ImageDraw.Draw(self.image)
        color = (255, 0, 0)  # Красный цвет (RGB формат)
        outline_width = 2  # Толщина контура

        top_left = (center_x - radius, center_y - radius)
        bottom_right = (center_x + radius, center_y + radius)
        draw.ellipse([top_left, bottom_right], outline=color, width=outline_width)

    def save_image(self, file_path):
        """
        Сохраняет изображение
        :param file_path: путь к файлу
        :return:
        """

        self.image.save(file_path)

    def image_channel(self, channel):
        """
        Получение канала изображения
        :param channel: Индекс выбранного канала
        :return: channel = 0: Красный канал изображения
        :return: channel = 1: Зелёный канал изображения
        :return: channel = 2: Синий канал изображения
        """
        try:
            image = self.image.convert("RGB")
            red, green, blue = image.split()
            empty_pixels = red.point(lambda _: 0)
            red_merge = Image.merge("RGB", (red, empty_pixels, empty_pixels))
            green_merge = Image.merge("RGB", (empty_pixels, green, empty_pixels))
            blue_merge = Image.merge("RGB", (empty_pixels, empty_pixels, blue))
            channels_list = [red_merge, green_merge, blue_merge]
            return channels_list[channel]

        except Exception as e:
            print(str(e))
