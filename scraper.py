from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def crawler(link):
    # 1) Configure the Markdown generator to ignore links
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,     # strip out [text](), leaving just the text
            "escape_html": False,
            "body_width": 80
        }
    )

    # 2) Exclude all <a> tags so no links are included in the DOM at all
    config = CrawlerRunConfig(
        markdown_generator=md_generator,
        excluded_tags=[],
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(link, config=config)

        if result.success:
            try:
                with open(f"outputs/{''.join(link.split("/"))}.txt", "w", encoding='utf-8') as file:
                    file.write(result.markdown)
            except Exception as e:
                print(f"Error creating file for link {link}: {e}")
                # Create a safe filename as fallback
                safe_filename = "output_" + str(hash(link))
                with open(f"outputs/{safe_filename}.txt", "w", encoding='utf-8') as file:
                    file.write(result.markdown)
        else:
            try:
                with open(f"outputs/{''.join(link.split("/"))}.txt", "w", encoding='utf-8') as file:
                    file.write("Crawl failed: " + result.error_message)
            except Exception as e:
                print(f"Error creating error file for link {link}: {e}")
                # Create a safe filename as fallback
                safe_filename = "error_" + str(hash(link))
                with open(f"outputs/{safe_filename}.txt", "w", encoding='utf-8') as file:
                    file.write("Crawl failed: " + result.error_message)

# if __name__ == "__main__":
#     asyncio.run(main())
