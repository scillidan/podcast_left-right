add $name:
	#!/bin/sh
	set -eu
	mkdir -p _output/txt _output/txt-no-punc _output/txt-pdf _output/txt-pdf-jpg _output/mp4 _output/srt-punc-to-spc
	if [ -f "medias/{{name}}.m4a" ]; then
		media="medias/{{name}}.m4a"
	elif [ -f "medias/{{name}}.mp3" ]; then
		media="medias/{{name}}.mp3"
	else
		echo "Error: media not found for {{name}} (.m4a or .mp3)"
		exit 1
	fi
	python scripts/srt_to_txt.py -i "_output/srt/{{name}}.srt" -o "_output/txt/{{name}}.txt"
	python scripts/txt_no_punc.py -i "_output/txt/{{name}}.txt" -o "_output/txt-no-punc/{{name}}.txt"
	python scripts/txt_gen_pdf.py -i "_output/txt-no-punc/{{name}}.txt" -o "_output/txt-pdf/{{name}}.typ"
	typst compile "_output/txt-pdf/{{name}}.typ" "_output/txt-pdf/{{name}}.pdf"
	magick -density 300 "_output/txt-pdf/{{name}}.pdf[0]" -resize x1080 -background white -alpha remove -quality 90 "_output/txt-pdf-jpg/{{name}}.pdf.jpg"
	ffmpeg -loop 1 -framerate 1 -i "_output/txt-pdf-jpg/{{name}}.pdf.jpg" -i "$media" -c:v libx264 -tune stillimage -c:a copy -pix_fmt yuv420p -shortest -y "_output/mp4/{{name}}.mp4"
	python scripts/srt_punc_to_spc.py -i "_output/srt/{{name}}.srt" -o "_output/srt-punc-to-spc/{{name}}.srt"
