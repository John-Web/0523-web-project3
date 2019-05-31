<template>
  <div id="app">
    <div id="wrapper" >
    <div id="content">
    <div>
      <span @click="all_movies(1)">
        <Icon type="ios-home" size="24" style="width: auto"/>
      </span>
      <Input placeholder="Search something..." v-model="search_text"
             @keyup.enter.native="search_movies()" style="width: auto"/>
      <Button type="primary" @click.native="search_movies()">搜索</Button>
    </div>
    <h2>{{message_text}}</h2>
    <div v-for="movie in movies">
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
    <Page id="page" :current="current_page" :total="data_count" :page-size="page_size"
          @on-change="change_page" show-elevator />
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
        init_page_size: 5,
        init_data_count: 10000,
        data_count: 10000,
        page_size: 5,
        current_page: 1,
        search_mode: false,
        search_text: '',
        message_text: ''
      };
    },
    created: function() {
      this.all_movies(1);
    },
    methods:{
      getImages( _url ){
        if( _url !== undefined ){
          let _u = _url.substring( 7 );
          return 'https://images.weserv.nl/?url=' + _u;
        }
      },
      all_movies (index) {
        this.message_text = "正在载入第" + this.current_page + "页";
        this.current_page = index;
        this.page_size = this.init_page_size;
        this.data_count = this.init_data_count;
        this.search_mode = false;
        const start_index = this.init_page_size * (index - 1);
        let params = new URLSearchParams();
        params.append('start_index', start_index.toString());
        params.append('page_size', this.init_page_size);
        this.axios.get('/api/all_movies', {params: params})
          .then((response) => {
            for (let i = 0; i < this.page_size; i++){
              response.data[i].poster = this.getImages(response.data[i].poster)
            }
            this.movies = response.data;
            this.message_text = "载入第" + this.current_page + "页完成";
          })
          .catch(function (error) {
            console.log(error);
            this.message_text = "载入第" + this.current_page + "页失败";
          });

      },
      search_movies () {
        const search_T = this.search_text;
        if(search_T == "") return;
        this.message_text = "正在查询包含关键字\"" + search_T + "\"的电影";
        this.search_mode = true;
        let params = new URLSearchParams();
        params.append('search_text', this.search_text);
        this.axios.get('/api/search_movies', {params: params})
          .then((response) => {
            this.data_count  = response.data.length;
            this.page_size  = response.data.length;
            for (let i = 0; i < this.page_size; i++){
              response.data.movies[i].poster = this.getImages(response.data.movies[i].poster)
            }
            this.movies = response.data.movies;
            this.message_text = "查询到包含关键字\"" + search_T + "\"的电影共" + response.data.length + "条";
          })
          .catch(function (error) {
            console.log(error);
            this.message_text = "查询到包含关键字\"" + search_T + "\"的电影失败";
          });
      },
      change_page(index){
        if(this.search_mode == false){
          this.all_movies(index);
        }
      }
    }
  }
</script>

<style>
  @import "douban.css";
  #mainpic img { max-width: 135px }
</style>
