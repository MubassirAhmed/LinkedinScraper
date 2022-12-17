import extract, initialize_db
#import _transform

if __name__ == "__main__":
    s3filename = extract.main()
    
    #wait until scraper finished doing its job
    initialize_db.main(s3filename)
    
    #_transform.main()
    #load.main()