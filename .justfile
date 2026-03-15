default:
	just update

update:
	python script/update.py

batch:
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
	find txt-pdf-jpg -maxdepth 1 -name "*.jpg" -print0 | sort -z | while IFS= read -r -d '' f; do \
		basename=$(basename "$f" .jpg | sed 's/\.pdf//g'); \
		img_file="$f"; \
		aud_file="${basename}.m4a"; \
		if [ -f "$aud_file" ] && [ ! -f "mp4/${basename}.mp4" ]; then \
			ffmpeg -loop 1 -framerate 1 -i "$img_file" -i "$aud_file" -c:v libx264 -tune stillimage -c:a copy -pix_fmt yuv420p -shortest -y "mp4/${basename}.mp4" || echo "FAILED: $basename"; \
		fi; \
	done

srt:
    python script/srt_punc_to_spc.py srt/ srt_punc_to_spc/

clear:
	rm txt-pdf/*.typ