const fs = require('fs')
const path = require('path')
const { HLTV } = require('hltv')

const dataDirectory = path.join(__dirname)

if (!fs.existsSync(dataDirectory)) {
    fs.mkdirSync(dataDirectory)
}

const newsFilePath = path.join(dataDirectory, 'news.json')
const errorFilePath = path.join(dataDirectory, 'error.json')

HLTV.getNews({ 'year': 2023, 'month': 'september' })
    .then((res) => {
        fs.writeFileSync(newsFilePath, JSON.stringify(res, null, 2))
        console.log('News data saved to news.json')
    })
    .catch((err) => {
        fs.writeFileSync(errorFilePath, JSON.stringify(err, null, 2))
        console.error('Error data saved to error.json')
    })

