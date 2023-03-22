from functions import box_score, get_game_links

    
start = 2021
end = 2022
outputpath = r'/home/stvn/Desktop/stats_reference_scrape/nba_box_scores/outputs/'

def scrape():
    
    box_score_urls = get_game_links(start, end)
    jj = 1
    for x in box_score_urls:
        error_urls = []
        try:
            print(f"working on file {jj} out of {len(box_score_urls)}")
            r = box_score(x)
            r.to_csv(outputpath + r.name)
            jj += 1
        except:
            print(f'error with {x}')
            error_urls.append(x)
            jj += 1
            continue
    return error_urls
    
if __name__ == "__main__":
    scrape()