<h1>Проект SNL_Crypt</h1>
<p>Описание: Проект SNL_Crypt предоставляет набор инструментов для шифрования и дешифрования данных, включая текстовые сообщения, файлы и целые диски. Он использует алгоритм AES-256 для обеспечения высокой степени безопасности данных. Проект распространяется под лицензией SNL_License.</p>

<h2>Возможности</h2>
<h3>Шифрование и Дешифрование Текста</h3>
<ul>
<li>Шифрование: Программа позволяет шифровать текстовые сообщения с использованием алгоритма AES. Сгенерированный ключ для шифрования сохраняется вместе с зашифрованным текстом.</li>
<li>Дешифрование: Пользователь может расшифровать текст, предоставив зашифрованное сообщение и ключ в формате base64.</li>
</ul>
<h3>Шифрование и Дешифрование Файлов</h3>
<ul>
<li>Шифрование Файлов: Программа позволяет зашифровывать файлы, при этом расширение файла не меняется.</li>
<li>Дешифрование Файлов: Пользователь может восстановить оригинальные файлы, предоставляя ключ для дешифрования.</li>
</ul>
<h3>Шифрование и Дешифрование Дисков</h3>
<ul>
<li>Шифрование Дисков: Позволяет зашифровывать все файлы на выбранном диске. Каждый зашифрованный файл получает расширение .SDE. Генерируется лог-файл с ключами для каждого файла, который впоследствии может быть использован для восстановления данных.</li>
<li>Дешифрование Дисков: Используя лог-файл и пароль, программа восстанавливает оригинальные файлы, зашифрованные на диске. Удаляет временные зашифрованные файлы для повышения безопасности.</li>
</ul>
<h2>Установка и Запуск</h2>
<ol>
<li>Убедитесь, что установлены все необходимые зависимости, включая библиотеку pycryptodome и tqdm.</li>
<li>Скачайте или клонируйте репозиторий на свой компьютер.</li>
<li>Доступны исполняемые файлы (.exe) как в установочной (сетап) версии, так и в портативной версии.</li>
<li>Запустите соответствующий скрипт или .exe файл для шифрования или дешифрования в зависимости от ваших нужд.</li>
</ol>
<h3>Примечания</h3>
<ul>
<li>SNL_Crypt в некоторых случаях требует прав администратора для шифрования дисков.</li>
<li>Все ключи для шифрования дисков и зашифрованные данные хранятся безопасно и защищены от несанкционированного доступа.</li>
<li>Ключ-файл для шифрования файлов хранится в папке программы в под-папке FILE_CRYPT</li>
<li>Зишифрованный тест и ключ к нему хранятся в однов файле</li>
<li>При первом запуске шифрования файлов требуются права администратора что бы создать ключ-файл</li>
<li>При шифровании диска файлы становятся в 2 раза больше в объеме</li>
</ul>
<br>
<h1>P.S</h1>
<h3>Вот вам пасхалочка</h3>
<p>Текст:<br>U1VPtGR0ukwNOYoYjsLZq7Tn0ghjgk4sAGMce/oNtAgdg9jkAzELGQOzZkSGhESxapLkyfEr4iwDct1SWWip9XZ7aL1SmCxT/9MqBzeCavIGRGYM3Tdv8tJlwbI7OmaOpG1CDwPAHDzcoFud1u2DcbC/px88gbe2QUfAwwwxs05e2u/7AzCns3Zqf6MM7Greqsemfvhx6VaUxWgO3PQGSISwFIQ9V2y6olbhpSn+sudy8exnY3NMWY3DFqaM9JofY2JmnXp/+SZlYnFaITqGVuS0MbwJlp5/MTEJkNdDZBj2</p>
<p>Ключ:<br>hBfFoleVJIVZ5IERkp4Ff7S0xwLjAqCuWrHxhiPfIjk=</p>
<h3>P.P.S</h3>
<p>Для расшифровки требуется моя программа</p>
