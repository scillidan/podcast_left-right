default:
	just update

update:
	@for f in *.m4a; do \
		name=`echo "$$f" | sed 's/\.m4a$$//'`; \
		if [ ! -f "mp4/$$name.mp4" ] && [ -f "txt/$$name.txt" ]; then \
			echo "Processing $$name"; \
			just add "$$name"; \
		fi; \
	done

add $name:
	python script/txt_no_punc.py -i "txt/{{name}}.txt" -o "txt_no_punc/{{name}}.txt"
	python script/txt_gen_pdf.py -i "txt_no_punc/{{name}}.txt" -o "txt-pdf/{{name}}.typ"
	typst compile "txt-pdf/{{name}}.typ" "txt-pdf/{{name}}.pdf"
	magick -density 300 "txt-pdf/{{name}}.pdf[0]" -resize x1080 -background white -alpha remove -quality 90 "txt-pdf-jpg/{{name}}.pdf.jpg"
	ffmpeg -loop 1 -framerate 1 -i "txt-pdf-jpg/{{name}}.pdf.jpg" -i "{{name}}.m4a" -c:v libx264 -tune stillimage -c:a copy -pix_fmt yuv420p -shortest -y "mp4/{{name}}.mp4"
	python script/srt_punc_to_spc.py -i "srt/{{name}}.srt" -o "srt_punc_to_spc/{{name}}.srt"

txt $name:
	python script/txt_no_punc.py -i "txt/{{name}}.txt" -o "txt_no_punc/{{name}}.txt"

txt-pdf $name:
	python script/txt_gen_pdf.py -i "txt_no_punc/{{name}}.txt" -o "txt-pdf/{{name}}.typ"
	typst compile "txt-pdf/{{name}}.typ" "txt-pdf/{{name}}.pdf"

txt-pdf-jpg $name:
	magick -density 300 "txt-pdf/{{name}}.pdf[0]" -resize x1080 -background white -alpha remove -quality 90 "txt-pdf-jpg/{{name}}.pdf.jpg"

mp4 $name:
	ffmpeg -loop 1 -framerate 1 -i "txt-pdf-jpg/{{name}}.pdf.jpg" -i "{{name}}.m4a" -c:v libx264 -tune stillimage -c:a copy -pix_fmt yuv420p -shortest -y "mp4/{{name}}.mp4"

srt $name:
	python script/srt_punc_to_spc.py -i "srt/{{name}}.srt" -o "srt_punc_to_spc/{{name}}.srt"