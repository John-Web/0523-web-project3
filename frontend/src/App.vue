<template>
  <div id="app">
    <div id="wrapper" >
    <div id="content">
    <Icon type="ios-home" onclick="this.getJsonInfo()"/>
    <Input search placeholder="Enter something..." />
    <div v-for="(movie, index) in movies">
    <div v-if="index >= start_index && index < end_index">
    <h1>
      <span property="v:itemreviewed">{{movie.title}}</span>
      <span class="year">({{movie.year}})</span>
    </h1>
    <div class="subjectwrap clearfix">
      <div class="subject clearfix">
        <div id="mainpic" class="">
          <img :src="movie.poster" :alt="movie.title" rel="v:image">
        </div>
        <div id="info">
          <span><span class="pl">导演</span>:
            <span class="attrs" v-for="(director,director_index) in movie.directors">
              <span v-if="director_index !== 0"> /</span>
              <a :href="[site + 'celebrity/'+ director.id + '/']" rel="v:directedBy">{{director.name}}</a>
            </span>
          </span><br>

          <span><span class="pl">编剧</span>:
            <span class="attrs" v-for="(writer,writer_index) in movie.writers">
              <span v-if="writer_index !== 0"> /</span>
              <a :href="[site + 'celebrity/'+ writer.id + '/']">{{writer.name}}</a>
            </span>
          </span><br>

          <span class="actor"><span class="pl">主演</span>:
            <span class="attrs" v-for="(cast,cast_index) in movie.casts">
              <span v-if="cast_index !== 0"> /</span>
              <a :href="[site + 'celebrity/'+ cast.id + '/']" rel="v:starring">{{cast.name}}</a>
            </span>
          </span><br>

          <span class="pl">类型:</span>
          <span property="v:genre" v-for="(genre,genre_index) in movie.genres">
            <span v-if="genre_index !== 0"> /</span>
            {{genre}}
          </span><br>

          <span class="pl">制片国家/地区:</span>
          <span v-for="(country,country_index) in movie.countries">
            <span v-if="country_index !== 0"> /</span>
            {{country}}
          </span><br>

          <span class="pl">语言:</span>
          <span v-for="(language,language_index) in movie.languages">
            <span v-if="language_index !== 0"> /</span>
            {{language}}
          </span><br>

          <span class="pl">上映日期:</span>
          <span property="v:initialReleaseDate" v-for="(pubdatee,pubdatee_index) in movie.pubdate">
            <span v-if="pubdatee_index !== 0"> /</span>
            {{pubdatee}}
          </span><br>

          <span class="pl">片长:</span>
          <span property="v:runtime">{{movie.duration}}分钟</span><br>

          <span class="pl">IMDb链接:</span>
          <a :href="['http://www.imdb.com/title/' + movie.imdb]" target="_blank" rel="nofollow">{{movie.imdb}}</a><br>
        </div>
      </div>
      <div id="interest_sectl">
        <div class="rating_wrap clearbox" rel="v:rating" >
          <div class="clearfix">
            <div class="rating_logo ll">豆瓣评分</div>
          </div>
          <div class="rating_self clearfix" typeof="v:Rating">
            <strong class="ll rating_num" property="v:average">{{movie.ratingAverage}}</strong>
            <span property="v:best" content="10.0"></span>
            <div class="rating_right ">
              <div class="ll bigstar bigstar35"></div>
              <div class="rating_sum">
                <a href="collections" class="rating_people"><span property="v:votes">{{movie.ratingPeople}}</span>人评价</a>
              </div>
            </div>
          </div>
          <div class="ratings-on-weight">
            <div class="item">
              <span class="stars5 starstop" title="力荐">
                5星
              </span>
              <div class="power" :style="{'width': movie.star5*rating_power_coefficient + 'px'}"></div>
              <span class="rating_per">{{movie.star5}}%</span>
              <br>
            </div>
            <div class="item">
              <span class="stars4 starstop" title="推荐">
                4星
              </span>
              <div class="power" :style="{'width': movie.star4*rating_power_coefficient + 'px'}"></div>
              <span class="rating_per">{{movie.star4}}%</span>
              <br>
            </div>
            <div class="item">
              <span class="stars3 starstop" title="还行">
                3星
              </span>
              <div class="power" :style="{'width': movie.star3*rating_power_coefficient + 'px'}"></div>
              <span class="rating_per">{{movie.star3}}%</span>
              <br>
            </div>
            <div class="item">
              <span class="stars2 starstop" title="较差">
                2星
              </span>
              <div class="power" :style="{'width': movie.star2*rating_power_coefficient + 'px'}"></div>
              <span class="rating_per">{{movie.star2}}%</span>
              <br>
            </div>
            <div class="item">
              <span class="stars1 starstop" title="很差">
                1星
              </span>
              <div class="power" :style="{'width': movie.star1*rating_power_coefficient + 'px'}"></div>
              <span class="rating_per">{{movie.star1}}%</span>
              <br>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
    </div>
      <Page id="page" :total="data_count" :page-size="page_size" @on-change="change_page" show-elevator />
    </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'app',
    data: function(){
      return {
        movies: '',
        site: "https://movie.douban.com/",
        rating_power_coefficient: 1.2,

        data_count: 200,
        page_size: 5,
        start_index: 0,
        end_index: 5
      }
    },
    created: function() {
      this.getJsonInfo()
    },
    methods:{
      getImages( _url ){
        if( _url !== undefined ){
          let _u = _url.substring( 7 );
          return 'https://images.weserv.nl/?url=' + _u;
        }
      },
      getJsonInfo () {
      let params = new URLSearchParams();
      params.append('start_index', this.start_index);
      params.append('page_size', this.page_size);
      this.axios.get('/api/getJsonInfo', {params: params})
        .then((response) => {
          for (let i = 0; i < this.page_size; i++){
            response.data[i].poster = this.getImages(response.data[i].poster)
          }
          this.movies = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      change_page(index){
        this.start_index = this.page_size * (index - 1);
        this.end_index = this.page_size * index;
      }
    }
  }
</script>

<style>
  @import "douban.css";
  #mainpic img { max-width: 135px }
</style>
