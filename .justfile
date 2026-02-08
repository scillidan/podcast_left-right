default:
	just all

all:
	just txt
	just txt-pdf
	just txt-pdf-jpg
	just mp4
	just srt

txt:
    python script/txt_no_punc.py txt/ txt_no_punc/

txt-pdf:
    python script/txt_gen_pdf.py txt_no_punc/ txt-pdf/
    for f in txt-pdf/*.typ; do typst compile "$f" "${f%.typ}.pdf"; done

txt-pdf-jpg:
	mkdir -p txt-pdf-jpg
	for f in txt-pdf/*.pdf; do \
		basename=$(basename "$f" .pdf); \
		magick -density 300 "$f[0]" -resize x1080 -background white -alpha remove -quality 90 "txt-pdf-jpg/$basename.pdf.jpg"; \
	done

mp4:
	mkdir -p mp4
	find txt-pdf-jpg -maxdepth 1 -name "*.jpg" -print0 | while IFS= read -r -d '' f; do \
		basename=$(basename "$f" .pdf.jpg | sed 's/｜/|/g'); \
		img_file="$f"; \
		aud_file="${basename}.m4a"; \
		if [ -f "$aud_file" ]; then \
			ffmpeg -loop 1 -framerate 1 -i "$img_file" -i "$aud_file" -c:v libx264 -tune stillimage -c:a copy -pix_fmt yuv420p -shortest -y "mp4/${basename}.mp4"; \
		fi; \
	done

srt:
    python script/srt_punc_to_spc.py srt/ srt_punc_to_spc/

clear:
	rm txt-pdf/*.typ

add basename:
	@mkdir -p txt_no_punc txt-pdf txt-pdf-jpg mp4 srt_punc_to_spc
	@audio_file="" && \
	for ext in m4a mp3; do \
		if [ -f "{{basename}}.$$ext" ]; then \
			audio_file="{{basename}}.$$ext"; \
			break; \
		fi; \
	done
	python script/txt_no_punc.py "txt/{{basename}}.txt" "txt_no_punc/{{basename}}.txt"
	python script/txt_gen_pdf.py "txt_no_punc/{{basename}}.txt" "txt-pdf/{{basename}}.typ"
	@typst compile "txt-pdf/{{basename}}.typ" "txt-pdf/{{basename}}.pdf" 2>/dev/null
	@if [ -f "txt-pdf/{{basename}}.pdf" ]; then \
		magick -density 300 "txt-pdf/{{basename}}.pdf[0]" -resize x1080 \
			-background white -alpha remove -quality 90 \
			"txt-pdf-jpg/{{basename}}.pdf.jpg" 2>/dev/null; \
	fi
	@if [ -n "$$audio_file" ] && [ -f "txt-pdf-jpg/{{basename}}.pdf.jpg" ]; then \
		ffmpeg -loop 1 -framerate 1 -i "txt-pdf-jpg/{{basename}}.pdf.jpg" \
			-i "$$audio_file" -c:v libx264 -tune stillimage -c:a copy \
			-pix_fmt yuv420p -shortest -y "mp4/{{basename}}.mp4" 2>/dev/null; \
	fi
	python script/srt_punc_to_spc.py "srt/{{basename}}.srt" "srt_punc_to_spc/{{basename}}.srt"
	@echo "✅ {{basename}}"