Vue.component('coursebox',{
  template:'#course',
  props:['course'],
  mounted:()=>{
    // console.log(this.course)
  }
});
const vm = new Vue({
  el:'#app',
  data:{
    faculties:['全部','文學院','理學院','社科院','工學院','管學院','法學院','教育學院','其他'],
    codes:[],
    courses:[],
    state:'0',
    filter:'',
  },
  mounted:function() {
    $.getJSON("code_table.json").then((res)=>{
      this.codes = res;
      console.log("code read sucessly");
    });
    $.getJSON("courses.json").then((res)=>{
      this.courses = res
      console.log("courses read sucessly");
    });
  },
  methods:{
    change_state(id){
      console.log(id);
      this.state = id;
      let $opt = $('.opt');
      console.log($opt);

      Array.from($opt).forEach((i)=>{
        console.log(i);
        $(i).removeClass('highlight');
      });
      $opt = $($opt.get(id));
      $opt.addClass('highlight');
    }
  },
  computed:{
    filter_courses:function () {
      let results=[];
      for(department in this.courses){
        if((!(department.match(new RegExp('^[a-z]','i'))&&this.state=='8'))&&(this.state!=department[0])&&this.state!='0') continue;
        this.courses[department].forEach((course)=>{
          const flag = course.class_name.toLowerCase().indexOf(this.filter.toLowerCase());
          if(flag!=-1){
            course['faculty'] = this.codes[department];
            results.push(course);
          }
        });
      }
      return results;
    },
  }
});
